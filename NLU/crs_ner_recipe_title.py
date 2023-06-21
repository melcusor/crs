import pathlib

import spacy
import re
from pathlib import Path
from NLU.CONSTANTS import SPACY_DE_STOPWORDS, RECIPE_TITLE_ENTITY_REPLACEMENT, SPACY_NER_MODEL_PATH
from NLU.pattern_matcher import PatternMatcher


def _clean_recipe_title(recipe_title):
    recipe_title = re.sub('\W+', ' ', recipe_title)
    recipe_title = re.sub('\d+', ' ', recipe_title)

    recipe_title = recipe_title.lower()
    return ' '.join([word for word in recipe_title.split() if word not in SPACY_DE_STOPWORDS])


class NERRecipeTile:
    def __init__(self):
        print("Loading SPACY model")

        path = pathlib.Path().parent.resolve() / SPACY_NER_MODEL_PATH
        self.spacy_ner_model = spacy.load(path)

        self.matcher = PatternMatcher()

    def get_recipe_title(self, utterance):
        print("checking if ne recipe_title in utterance")
        doc = self.spacy_ner_model(utterance)
        recognized = doc.ents

        print("NERRecipeTitle - entities: ", type(recognized), recognized)
        recognized_in = []
        recognized_out = []

        # check which titles are preferred / to be left out using the same pattern matcher as for all other entities

        for title in recognized:
            title = str(title)
            print("recognized title: ", type(title), title)
            utterance_with_replacement = re.sub(title, RECIPE_TITLE_ENTITY_REPLACEMENT, utterance)
            negative_matches = self.matcher.match_neg_ingredient_patterns(utterance_with_replacement.lower(),
                                                                          [RECIPE_TITLE_ENTITY_REPLACEMENT.lower()])

            print("RECIPE TITLE NEGATIVE MATCHES:")
            print(type(negative_matches), negative_matches)

            title = _clean_recipe_title(title)

            if "None" in negative_matches:
                if title not in recognized_in:
                    recognized_in = [title]
            else:
                if title in recognized_in:
                    recognized_in = []
                if title not in recognized_out:
                    recognized_out.append(title)

        return {"entities_in": recognized_in,
                "entities_out": recognized_out}
