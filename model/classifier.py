import torch
import torch.nn as nn
import torch.nn.functional as F


class LSTMAttentionClassifier(nn.Module):
    def __init__(
        self,
        emb_matrix,
        n_classes,
        freeze,
        hidden=128,
        num_layers=1,
        bidirectional=True,
        dropout=0.3,
    ):
        super().__init__()
        self.bidirectional = bidirectional
        self.hidden_size = hidden
        self.num_directions = 2 if bidirectional else 1

        self.embedding = nn.Embedding.from_pretrained(
            torch.tensor(emb_matrix), freeze=freeze
        )

        self.lstm = nn.LSTM(
            input_size=emb_matrix.shape[1],
            hidden_size=hidden,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=bidirectional,
            dropout=dropout if num_layers > 1 else 0,
        )

        self.attention = nn.Linear(hidden * self.num_directions, 1)

        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden * self.num_directions, n_classes)

    def forward(self, x, lengths):
        emb = self.embedding(x)

        packed = nn.utils.rnn.pack_padded_sequence(
            emb, lengths.cpu(), batch_first=True, enforce_sorted=False
        )
        packed_out, _ = self.lstm(packed)
        lstm_out, _ = nn.utils.rnn.pad_packed_sequence(packed_out, batch_first=True)

        attn_weights = self.attention(lstm_out)
        attn_weights = torch.softmax(attn_weights.squeeze(-1), dim=1).unsqueeze(-1)

        context = torch.sum(lstm_out * attn_weights, dim=1)

        out = self.dropout(context)
        logits = self.fc(out)
        return logits
