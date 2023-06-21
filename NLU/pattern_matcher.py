from spacy.matcher import Matcher
import spacy


class PatternMatcher:
    def __init__(self):
        #print("Init PatternMatcher class...")

        self.nlp = spacy.load("de_core_news_sm")
        #print("All pipes: ", self.nlp.pipe_names)

        self.nlp.remove_pipe("tagger")
        self.nlp.remove_pipe("ner")
        self.nlp.remove_pipe("attribute_ruler")
        #print("Cleaned: ", self.nlp.pipe_names)

        self.matched_strings = []

    def match_neg_ingredient_patterns(self, user_input, recognized_entities_list):
        """

        # ist ohne Zwiebeln / hat keine Tomaten drin => ich möchte sie aber drin haben! =>
        # this should not be recognized as negative pattern, so we negate sein
        ing_pattern_neg_0 = [
            {'LEMMA': {'IN': ["sein", "haben"]}, 'OP': '!'},
            {'LEMMA': {'IN': ['kein', 'ohne']}, 'OP': '+'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '+'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '*'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '*'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '*'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '*'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '*'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '*'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'LOWER': {'IN': ['daheim', 'da', 'zuhause', 'rein', 'im Rezept', 'vorhanden', 'drin']}, 'OP': '*'}
        ]
        """

        # KEIN [e|en] X [,] [Y] [DAHEIM | DA | ZUHAUSE | REIN | IM REZEPT | VORHANDEN]
        ing_pattern_neg_1 = [
            {'LEMMA': {'IN': ['kein', 'ohne']}, 'OP': '+'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '+'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '*'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '*'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '*'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '*'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '*'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '*'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'LOWER': {'IN': ['daheim', 'da', 'zuhause', 'rein', 'im Rezept', 'vorhanden', 'drin']}, 'OP': '*'}
        ]


        # WEDER X [,] NOCH Y
        ing_pattern_neg_2 = [
            {'LEMMA': 'weder'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '+'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},

            {'LEMMA':{'IN':['noch', 'oder']}, 'OP': '+'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '+'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},

            {'LEMMA':{'IN':['noch', 'oder']}, 'OP': '*'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '*'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'}
        ]

        # MAG | ESSE | MÖCHTE | KOCHE | NEHME | VERTRAGE | ERTRAGE | BEREITE| KANN [KEIN | OHNE] INGRED_ENT [ESSEN | VERTRAGEN | NEHMEN | KOCHEN | ZUBEREITEN | ZU]
        ing_pattern_neg_3 = [
            {'LEMMA': {
                'IN': ['mögen', 'essen', 'möchten', 'kochen', 'nehmen', 'vertragen', 'ertragen', 'bereiten', 'können']},
             'OP': '+'},
            {'LEMMA': {'IN': ['nix', 'nichts', 'kein', 'ohne']}, 'OP': '+'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '+'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '*'},
            {'ORTH': 'und', 'OP': '*'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '*'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '*'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '*'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'LEMMA': {'IN': ['essen', 'kochen', 'nehmen', 'vertragen', 'ertragen', 'zubereiten']}, 'OP': '*'},
            {'ORTH': {'IN': ['zu']}, 'OP': '*'}
        ]

        # MAG | ESSE | MÖCHTE | KOCHE | NEHME | BEREITE| KANN [KEIN, KEINE, KEINEN] INGRED_ENT [NICHT] [ESSEN | VERTRAGEN | NEHMEN | KOCHEN | ZUBEREITEN | ZU]
        # KOCHE [MIT] INGRED_ENT NICHT
        ing_pattern_neg_4 = [
            {'LEMMA': {
                'IN': ['mögen', 'essen', 'möchten', 'kochen', 'nehmen', 'vertragen', 'ertragen', 'bereiten', 'können']},
             'OP': '+'},
            {'ORTH': 'mit', 'OP': '?'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '+'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '*'},
            {'ORTH': 'mit', 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '*'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '*'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '*'},
            {'ORTH': 'mit', 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '*'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '*'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'LOWER': {'IN': ['nicht', 'nie', 'niemals']}, 'OP': '+'},

            {'LEMMA': {'IN': ['essen', 'kochen', 'nehmen', 'vertragen', 'ertragen', 'zubereiten']}, 'OP': '?'},
            {'ORTH': {'IN': ['zu']}, 'OP': '?'}
        ]

        # ICH HASSE X
        ing_pattern_neg_5 = [
            {'LEMMA': {'IN': ['hassen']}, 'OP': '+'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '+'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '*'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '*'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},
        ]

        # X schmeckt | geht | mag | nehme | esse | möchte | finde [ich | mir] [überhaupt | gar] nicht [gut]
        ing_pattern_neg_6 = [
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '+'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '?'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '?'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'LEMMA': {'IN': ['schmecken', 'gehen', 'mögen', 'nehmen', 'essen', 'möchten', 'finden']}, 'OP': '+'},

            {'LEMMA': {'IN': ['ich', 'mir', 'wir', 'uns']}, 'OP': '+'},
            {'LEMMA': {'IN': ['überhaupt', 'gar']}, 'OP': '?'},
            {'ORTH': 'nicht', 'OP': '+'},
            {'ORTH': 'gut', 'OP': '?'}
        ]

        # INGRED_ENT [WÜRDE | KÖNNTE | MÖCHTE] [ICH] [NICHT | NIE | NIEMALS] [NEHMEN | BENUTZEN | ESSEN | KOCHEN | ZUBEREITEN]
        # INGRED_ENT [WÜRDE] [ICH] vermeiden | weg lassen | weglasen
        ing_pattern_neg_7 = [
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '+'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '?'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '?'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'LEMMA': {'IN': ['möchten', 'werden', 'können']}, 'OP': '?'},
            {'LEMMA': 'ich', 'OP': '?'},
            {'LEMMA': {'IN': ['nicht', 'nie', 'niemals']}, 'OP': '?'},

            {'LEMMA': {'IN': ['nehmen', 'benutzen', 'essen', 'kochen', 'zubereiten', 'vermeiden', 'weglassen', 'weg',
                       'auslassen']}, 'OP': '+'}
        ]

        #  mir schmeckt INGRED_ENT nicht
        ing_pattern_neg_8 = [
            {'ORTH': {'IN': ['mir', 'uns']}, 'OP': '+'},
            {'LEMMA': {'IN': ['schmecken', 'gefallen']}, 'OP': '+'},

            {'ORTH': {'IN': recognized_entities_list}, 'OP': '+'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},
            {'IS_PUNCT': True, 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '?'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '?'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'LEMMA': {'IN': ['überhaupt', 'gar']}, 'OP': '?'},
            {'ORTH': 'nicht', 'OP': '+'}

        ]

        # ALLERGIE | INTOLERANZ | UNVERTRÄGLICHKEIT | ALLERGISCH | EMPFINDLICH [GEGEN | AUF | GEGENÜBER] X
        ing_pattern_neg_9 = [
            {'LEMMA': {'IN': ['allergie', 'intoleranz', 'unverträglichkeit', 'allergisch', 'empfindlich']}, 'OP': '+'},
            {'ORTH': {'IN': ['gegen', 'auf', 'gegenüber']}, 'OP': '+'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '+'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '?'},
            {'ORTH': {'IN': ['gegen', 'auf', 'gegenüber']}, 'OP': '?'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '?'},
            {'ORTH': {'IN': ['gegen', 'auf', 'gegenüber']}, 'OP': '?'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'}
        ]

        # NICHT [MIT] INGRED_ENT
        ing_pattern_neg_10 = [
            {'LEMMA': {'IN': ['nix', 'nichts', 'nicht', 'nie', 'niemals']}, 'OP': '+'},
            {'ORTH': 'mit', 'OP': '?'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '+'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '?'},
            {'ORTH': 'mit', 'OP': '?'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'},

            {'IS_PUNCT': True, 'OP': '?'},
            {'ORTH': {'IN': ['und', 'oder']}, 'OP': '?'},
            {'ORTH': 'mit', 'OP': '?'},
            {'ORTH': {'IN': recognized_entities_list}, 'OP': '?'},
            {'LEMMA': {'IN': ['Gericht', 'Rezept', 'Empfehlung', 'Essen', 'Produkt']}, 'OP': '?'}
        ]

        matcher = Matcher(self.nlp.vocab)

        matcher.add("INGREDIENT_OUT", [ing_pattern_neg_1, ing_pattern_neg_2, ing_pattern_neg_3,
                                       ing_pattern_neg_4, ing_pattern_neg_5, ing_pattern_neg_6,
                                       ing_pattern_neg_7, ing_pattern_neg_8, ing_pattern_neg_9,
                                       ing_pattern_neg_10])
        self.matched_strings = []

        matched_str = None
        doc = self.nlp(user_input)

        for match_id, start, end in matcher(doc):
            # print(doc[start:end])
            matched_str = doc[start:end]
        self.matched_strings.append(str(matched_str))

        # print("in pattern matcher class, matched strings: ", self.matched_strings)
        return self.matched_strings

