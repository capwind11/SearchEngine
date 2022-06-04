import re
import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from entity.global_entity import global_db
from transformers import BertTokenizer
from transformers import BertForSequenceClassification as BertModel

__all__ = ["classify_docs", "LABEL_MAP", "REV_LABEL_MAP"]

PAD = "[PAD]"
CLS = "[CLS]"

PRETRAINED_WEIGHTS = "bert-large-uncased"

LABEL_MAP = {
    "OTHERS": 0,
    "CRIME": 1,
    "ENTERTAINMENT": 2,
    "POLITICS": 3,
    "SPORTS": 4,
    "BUSINESS": 5,
    "TRAVEL": 6,
    "WELLNESS": 7,
    "FOOD & DRINK": 8,
    "SCIENCE & TECH": 9,
    "ARTS & CULTURE": 10
}

REV_LABEL_MAP = {
    0: "OTHERS",
    1: "CRIME",
    2: "ENTERTAINMENT",
    3: "POLITICS",
    4: "SPORTS",
    5: "BUSINESS",
    6: "TRAVEL",
    7: "WELLNESS",
    8: "FOOD & DRINK",
    9: "SCIENCE & TECH",
    10: "ARTS & CULTURE",
}


class NewsDataset(Dataset):
    def __init__(self, tokenizer, pad):
        super(NewsDataset, self).__init__()
        contents = self.prepare_data(tokenizer, pad)
        self.ids, self.token_type_ids, self.att_masks = contents

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, item):
        return self.ids[item], self.token_type_ids[item], self.att_masks[item]

    @staticmethod
    def prepare_data(tokenizer, pad):
        print(f"Preparing data from News Database ...")
        contents = list()
        # fetch from DB
        docs = global_db.query_all_docs()
        for doc in docs:
            ctx = doc[1].strip()  # title
            len_title = len(re.split(r"[ ]+", ctx))
            ctx += " " if ctx.endswith(".") else ". "
            content = doc[2].strip()  # content
            content_list = re.split(r"[ ]+", content)
            # we only consider the first 64 tokens when classifying
            content_list = content_list[:(64 - len_title)]
            content = " ".join(content_list)
            ctx += content
            contents.append(ctx)
        result = tokenizer(contents, padding=True, truncation=True,
                           max_length=pad, return_tensors="pt")
        print("Done.")
        return result["input_ids"], result["token_type_ids"], result["attention_mask"]


class BERT(nn.Module):
    def __init__(self, num_classes=11):
        super(BERT, self).__init__()
        self.tokenizer = BertTokenizer.from_pretrained(PRETRAINED_WEIGHTS)
        self.bert = BertModel.from_pretrained(
            PRETRAINED_WEIGHTS, num_labels=num_classes)

    def forward(self, x):
        ids, token_ids, att = x
        outputs = self.bert(input_ids=ids,
                            token_type_ids=token_ids,
                            attention_mask=att,
                            labels=None)
        return outputs.logits


def inference(model, test_loader, device):
    pred_labels = list()
    model.eval()
    with torch.no_grad():
        for i, data in enumerate(test_loader):
            ids, token_ids, att = data[:3]
            ids = ids.to(device)
            token_ids = token_ids.to(device)
            att = att.to(device)
            pred = model((ids, token_ids, att))
            y = pred.argmax(-1).cpu().numpy().tolist()
            pred_labels.extend(y)

    pred_classes = [REV_LABEL_MAP[i] for i in pred_labels]
    return pred_classes


def classify_docs(weights_path, device, save=False):
    """
    Classify the documents into 11 pre-defined categories using BERT.
    The 11 categories are shown in `LABEL_MAP` on top of this script.

    Args:
        weights_path: Specify the path to the trained weights.
            You can access the trained weights at this site:
            https://jbox.sjtu.edu.cn/l/h1PpOZ
        device: Specify the device to conduct classification. E.g.,
            'cpu` or 'cuda:0'.
        save: Specify whether to save the category into a txt file.

    Returns:
        A list of strings indicates the category of each document.
    """
    device = torch.device(device)
    model = BERT()
    ckpt = torch.load(weights_path, map_location="cpu")
    model.load_state_dict(ckpt)
    model = model.to(device)

    test_set = NewsDataset(model.tokenizer, pad=64)
    test_loader = DataLoader(test_set, 32, False, num_workers=4)
    pred_classes = inference(model, test_loader, device)
    # output the predicted category for each document in DB
    if save:
        # save the prediction to the txt file.
        with open(os.path.join(os.path.dirname(__file__), "../db/pred.txt"),
                  "w", encoding="utf-8") as f:
            for i in pred_classes:
                f.write(f"{i}\n")
    return pred_classes
