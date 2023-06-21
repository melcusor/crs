import os
import pathlib

import torch
import torch.nn

from transformers import AutoTokenizer
from NLU import CONSTANTS as C
from NLU.crs_transformers_bert_sentiment_classifier import BertClassifier

_tokenizer = AutoTokenizer.from_pretrained(C.TOKENIZER_FEEDBACK)
_tokenizer.add_special_tokens({'pad_token': '[PAD]'})

class FeedbackClassifier:
    def __init__(self):
        self.model = BertClassifier()

        path = pathlib.Path().parent.resolve() / C.FEEDBACK_CLASSIFICATION_MODEL_PATH / C.FEEDBACK_CLASSIFICATION_MODEL_NAME
        self.model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))

    def predict_feedback(self, user_input):
        text_dict = _tokenizer(user_input, padding='max_length', max_length=C.PADDING_MAX_LEN_SENT, truncation=True,
                               return_tensors="pt")
        use_cuda = torch.cuda.is_available()
        device = torch.device("cuda" if use_cuda else "cpu")
        #if use_cuda:
        model = self.model.to(device)
        mask = text_dict['attention_mask'].to(device)
        input_id = text_dict['input_ids'].squeeze(1).to(device)

        with torch.no_grad():
            output = model(input_id, mask)
            label_id = output.argmax(dim=1).item()

            for key in C.FEEDBACK_LABELS_DICTIONARY.keys():
                if C.FEEDBACK_LABELS_DICTIONARY[key] == label_id:
                    # print('PREDICTION: ', user_input, ' => ', key, '#', label_id)
                    break
        # print("Intent predicted by predict_intent method: ", key, label_id)
        return key, label_id
