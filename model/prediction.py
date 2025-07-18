import torch
import pickle
import numpy as np
import torch.nn.functional as F
from .classifier import LSTMAttentionClassifier
import spacy
from typing import List

nlp = spacy.load("en_core_web_sm")


def tokenize(text: str) -> List[str]:
    doc = nlp(text.lower())
    return [token.text for token in doc if not token.is_punct and token.is_alpha]


with open("model/vocab.pkl", "rb") as f:
    vocab = pickle.load(f)


def tokens_to_indices(tokens):
    return [vocab.get(token, vocab["<UNK>"]) for token in tokens]


with open("model/categories.pkl", "rb") as f:
    categories = pickle.load(f)

embedding_matrix = np.load("model/embedding_matrix.npy")
n_classes = len(categories)

model = LSTMAttentionClassifier(
    embedding_matrix,
    n_classes,
    freeze=True,
    hidden=128,
    num_layers=2,
    bidirectional=True,
)
model.load_state_dict(torch.load("model/best_model.pt", map_location="cpu"))
model.eval()


def predict(text: str):
    tokens = tokenize(text)
    indices = tokens_to_indices(tokens)
    length = torch.tensor([len(indices)])
    input_tensor = torch.tensor([indices])

    with torch.no_grad():
        logits = model(input_tensor, length)
        probs = F.softmax(logits, dim=1)
        pred_idx = probs.argmax(dim=1).item()
        return list(categories.keys())[list(categories.values()).index(pred_idx)]
