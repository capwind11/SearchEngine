from db.news_database import NewsDB
from service.utils import build_inverted_index


def test_query_by_doc_id():
    db_test = NewsDB()
    db_test.open_db()
    db_test.query_by_doc_id([1, 2, 3])
    db_test.close_db()


def test_query_by_specific_info():
    db_test = NewsDB()
    db_test.open_db()
    db_test.query_by_specific_info("2022-05-15", "globaltimes")
    db_test.close_db()


def test_query_by_specific_info():
    db_test = NewsDB()
    db_test.open_db()
    db_test.create_index_table()
    db_test.close_db()
    # db_test.query_by_specific_info("2022-05-15", "globaltimes")


def test_insert_index():
    db_test = NewsDB()
    db_test.open_db()
    build_inverted_index()
    db_test.close_db()


def test_query_index():
    db_test = NewsDB()
    db_test.open_db()
    res = db_test.query_doc_ids_by_word("test")
    print(res)
