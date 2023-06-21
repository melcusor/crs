import re
from unidecode import unidecode

from NLU.pattern_matcher import PatternMatcher
from recipesDBConnect.sql_alchemy_connect import KochbarDB

POSSIBLE_ADJ_ENDINGS = ['en', 'es', 'er', 'e']  # asiatisch/asiatisches
POSSIBLE_PLURAL_ENDINGS = ['nen', 'en', 'n', 'er', 's', 'se', 'e']  # Pilz/Pilze


def _unidecode_token(token):
    return unidecode(token)  # "äpfel" => "apfel"


class NER:
    def __init__(self, ingredients=None, cuisine=None, technique=None, menu_type=None):

        self.sql_db = KochbarDB()
        self.matcher = PatternMatcher()


    def sql_is_ne(self, token, table, column):
        if self.sql_db.sql_check_ne(token, table, column):
            return True
        # else:
        #    if table != "ingredients" and table != "diet_healthy":
        #        column = "syns"
        #        if self.sql_db.sql_check_ne(token, table, column):
        #            return True
        return False

    def ner_recognition(self, user_input, collection, field, replacement):
        # print("Searching in collection: ", collection)
        """
        :param replacement: keyword string to replace the found entity, needed for intent recognition
        :param user_input: user query string passed by the manager from the flask user interface
        :param collection: in which collection should the entity be searched for
        :param field: in which field of the collection above should be searched for
        :return: returns a dictionary with 2 lists for entities that:
                    - should be considered: "entities_in"
                    - should be left out by the recommender system: "entities_out"
        : how does it work: 2 STEPS:
        1. Split query in terms/tokens and check following:
            - if token "as is" is in given mongo collection
            - if unicode decoded token is in given mongo collection
            - if token has a plural ending, remove and check whether result or uni-decoded result are in mongo collection
            - if token has adj ending, remove it and check whether result or uni-decoded result are in mongo collection
            - if, when adding a plural ending, the result or uni-decoded result are in the mongo collection
        - case not considered: add adj ending and check result or uni-decoded result
        - if any matches found, these are added to the recognized list
        - for each match, if changes done to the token, replace original token in the user input

        2. Check for negative patterns in user input. We get them in form of a list of strings.
        For each recognized entity:
        - if entity in any of the negative patterns found, assign entity to "entities_out"
        - else assign entity to "entities_in"

        """

        # remove punctuation: https://www.geeksforgeeks.org/python-remove-punctuation-from-string/
        # user_input = re.sub(r'[^\w\s]', '', user_input)

        recognized = []

        recognized_in = []
        recognized_out = []
        temp_user_input = user_input
        # input_with_replacement = user_input.lower()

        for term in user_input.split():
            existent_plural_noun_ending = list(filter(str(term).endswith, POSSIBLE_PLURAL_ENDINGS))
            existent_adj_ending = list(filter(term.endswith, POSSIBLE_ADJ_ENDINGS))

            # Case 8:
            term = term.strip().lower()
            t_unidecode = _unidecode_token(term)

            # CHECK TOKEN AS IS - IF PRESENT IN INGREDIENTS' LIST
            if self.sql_is_ne(term, collection, field) and term not in recognized:
                recognized.append(term)
                # input_with_replacement = input_with_replacement.replace(term, replacement)
                # print("AS is: ", term)

            # CHECK UNI-DECODED TOKEN - IF PRESENT IN RESPECTIVE MONGODB COLLECTION/FIELD
            elif self.sql_is_ne(t_unidecode, collection, field) \
                    and t_unidecode not in recognized:
                recognized.append(t_unidecode)
                temp_user_input = temp_user_input.replace(term, t_unidecode)
                # input_with_replacement = input_with_replacement.replace(term, replacement)
            else:
                # CHECK IF TOKEN HAS A PLURAL ENDING AND REMOVE; CHECK PRESENCE IN RESPECTIVE MONGODB COLLECTION/FIELD
                if existent_plural_noun_ending:
                    # print("existent_ending: ", existent_ending)
                    for e in existent_plural_noun_ending:
                        t_temp = term[:-(len(e))]
                        t_unidecode_temp = t_unidecode[:-(len(e))]

                        if len(t_temp) != 0 and t_temp != "ei" and self.sql_is_ne(t_temp, collection, field):
                            if t_temp not in recognized:
                                # print("Plural Ending: ", t_temp)
                                recognized.append(t_temp)
                                temp_user_input = temp_user_input.replace(term, t_temp)
                                # input_with_replacement = input_with_replacement.replace(term, replacement)

                        if len(t_unidecode_temp) != 0 and t_unidecode_temp != "ei" and self.sql_is_ne(
                                t_unidecode_temp, collection, field):
                            if t_unidecode_temp not in recognized:
                                recognized.append(t_unidecode_temp)
                                temp_user_input = temp_user_input.replace(term, t_unidecode_temp)
                                # input_with_replacement = input_with_replacement.replace(term, replacement)

                for e in POSSIBLE_PLURAL_ENDINGS:
                    if self.sql_is_ne(term + e, collection, field) and term + e not in recognized:
                        recognized.append(term + e)
                        temp_user_input = temp_user_input.replace(term, term + e)
                        # input_with_replacement = input_with_replacement.replace(term, replacement)

                    if self.sql_is_ne(t_unidecode + e, collection, field) and term + e not in recognized:
                        recognized.append(t_unidecode + e)
                        temp_user_input = temp_user_input.replace(term, t_unidecode + e)
                        # input_with_replacement = input_with_replacement.replace(term, replacement)

                if existent_adj_ending:
                    for ending in existent_adj_ending:
                        t_temp = term[:-(len(ending))]
                        t_unidecode_temp = t_unidecode[:-(len(ending))]

                        if len(t_temp) != 0 and self.sql_is_ne(t_temp, collection, field) and t_temp not in recognized:
                            recognized.append(t_temp)
                            temp_user_input = temp_user_input.replace(term, t_temp)
                            # input_with_replacement = input_with_replacement.replace(term, replacement)

                        if len(t_unidecode_temp) != 0 and self.sql_is_ne(t_unidecode_temp, collection,
                                                                         field) and t_unidecode_temp not in recognized:
                            recognized.append(t_unidecode_temp)
                            temp_user_input = temp_user_input.replace(term, t_unidecode_temp)
                            # input_with_replacement = input_with_replacement.replace(term, replacement)
        # print("TEMP USER INPUT", temp_user_input)
        # print("INPUT WITH REPLACEMENT: ", input_with_replacement)
        # CHECK FOR NEGATIVE PATTERNS OF RECOGNIZED NAMED ENTITIES
        # OLD WAY, where we e.g. pass list with all ingredients:
        # negative_matches = self.matcher.match_neg_ingredient_patterns(temp_user_input.lower(), self.ingredients)
        # NEW WAY, where we pass only the list of already identified NE
        # negative matches is a list of matched expressions e.g. "habe keinen knoblauch da"
        negative_matches = self.matcher.match_neg_ingredient_patterns(temp_user_input.lower(), recognized)

        # TEST SQL QUERIES:
        for i in recognized:
            if self.sql_is_ne(i, collection, field):
                print("SQL NER CHECK: ", i)

        # CHECK HERE FOR MATCHES BETWEEN FOUND INGREDIENTS AND THE NEGATIVE INGREDIENT PATTERNS
        for ingredient in recognized:
            for match in negative_matches:
                if ingredient in match:
                    if ingredient not in recognized_out:
                        recognized_out.append(ingredient)
                else:
                    recognized_in.append(ingredient)
        return {"entities_in": recognized_in,
                "entities_out": recognized_out  # ,
                # "input_with_entity_replacement": input_with_replacement
                }

    def is_random_recipe(self):
        pass
