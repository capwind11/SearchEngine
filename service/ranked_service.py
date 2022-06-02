import os
import re

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from entity.global_entity import global_db
from service.utils import search_by_specific_info


def process_tfidf():
    docs = global_db.query_all_docs()
    contents = list()
    for doc in docs:
        ctx = doc[1].strip()  # title
        ctx += " " if ctx.endswith(".") else ". "
        content = doc[2].strip()  # content
        # we only consider the first 64 tokens when classifying
        ctx += content
        contents.append(ctx)
    # According to lecture slides, TF-iDF for documents should be LNC
    vectorizer_LNC = TfidfVectorizer(norm="l2", use_idf=False)
    X = vectorizer_LNC.fit_transform(contents)
    joblib.dump(X, f"../db/tfidf_LNC_dim{X.shape[1]}.pkl")
    # TF-iDF for query should be LTC, so we dump the LTC vectorizer
    # for future usage
    vectorizer_LTC = TfidfVectorizer(norm="l2", use_idf=True)
    vectorizer_LTC.fit(contents)
    joblib.dump(vectorizer_LTC, "../db/tfidf_LTC_vectorizer.pkl")


def get_ranked_ids(query, ids=None, minimum_hits=0):
    """
    Use TF-iDF to perform rank search given specific query.

    Notes:
        The list is 0-indexed. Need conversion for database usage.

    Args:
        query: String, the query.
        ids: List or None, if not None, the rank search will only consider
            the news items indexed in this list. Default: None.
        minimum_hits: Integer, specify the minimum number of hits.
            Default: 0.

    Returns:
        List, the sorted list computed by TF-iDF similarity indicating the
            indices of news items in the database.
    """
    # sparse matrix
    tfidf = joblib.load(
        os.path.join(os.path.dirname(__file__), "../db/tfidf_LNC_dim62504.pkl")
    )
    # search from the given ids
    if ids is not None:
        ids = np.array(ids)
        assert len(ids.shape) == 1
        tfidf = tfidf[ids]

    vectorizer = joblib.load(
        os.path.join(os.path.dirname(__file__), "../db/tfidf_LTC_vectorizer.pkl")
    )

    if minimum_hits > 0:
        query_token = [vectorizer.vocabulary_.get(i) for i in re.split(r"[ ]+", query)]
        query_token = np.array(query_token)
        target_cols = tfidf[:, query_token]
        cnts = np.count_nonzero(target_cols.toarray(), axis=1)
        selected_id = np.where(cnts >= minimum_hits)[0]
        tfidf = tfidf[selected_id]

    # (1, dim)
    query_vector = vectorizer.transform([query])
    scores = tfidf.dot(query_vector.T).todense()
    scores = np.array(scores).squeeze()
    # sort by decreasing order
    rank_list = np.argsort(scores, axis=0)[::-1]

    if minimum_hits > 0:
        return selected_id[rank_list]
    else:
        return rank_list


# 根据以下条件，执行rank搜索
def rank_search(
        keywords, source=None, date_begin=None, date_end=None, interval=None, cls=None
):
    if len(keywords) == 0:
        return None
    doc_ids = [i + 1 for i in get_ranked_ids(keywords)[:1000]]

    return search_by_specific_info(
        doc_ids, source, date_begin, date_end, interval, cls, True
    )
