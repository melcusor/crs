# MODEL outputs two variables:
# - The 1. variable, named _ , contains the embedding vectors of all of the tokens in a sequence.
# - The 2. variable, named pooled_output, contains the embedding vector of [CLS] token.
#   For a text classification task, it is enough to use this embedding as an input for our classifier.

from torch import nn
from transformers import BertModel


class BertClassifier(nn.Module):

    def __init__(self, dropout=0.5):
        super(BertClassifier, self).__init__()

        # self.bert = BertModel.from_pretrained('oliverguhr/german-sentiment-bert')
        self.bert = BertModel.from_pretrained('bert-base-german-cased')

        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768, 3)  # 3 is the output size, the number of labels present in the dataset
        self.relu = nn.ReLU()

    def forward(self, input_id, mask):
        _, pooled_output = self.bert(input_ids=input_id, attention_mask=mask, return_dict=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)
        final_layer = self.relu(linear_output)

        return final_layer
