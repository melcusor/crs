#################
# SYSTEM PROMPTS:
#################

# The first state S1 is overwritten by socketIO.on('status'), see crs.html
import os

STATES_SYSTEM_PROMPTS = {"S1": [  # "Hallo! Was kann ich für dich tun?",
    "Auf was hast du Lust?",
    "Was möchtest du kochen?",
    "Was würdest du gerne kochen/essen?",
    "Was für ein Rezept hättest du gerne?",
    "Was für ein Gericht hättest du denn gerne?"],

    # NOT USED
    # "Wie viel Zeit hast du zum Kochen", => preparation time
    # "Wie würdest du deine Kochfertigkeiten einschätzen?", => competency
    # "Erwartest du Besuch oder kochst du für dich alleine?", => servings
    # "Wie ausgefallen darf das Rezept sein", => recipe complexity
    # "Möchtest du ein Rezept für eine Hauptspeise?" => menu
    # "Gibt es Allergiker?", => diet_healty
    # "Welche Zutaten würdest du niemals benutzen?" => ingredients_out
    # "Gibt es Veganer oder Vegetarier?"
    # "Zu was für Rezepten greifst du normalerweise, wenn du etwas kochen möchtest?" => diet_healthy
    # CUISINE
    "S2.1": [  # "Wie stehst du zu regionaler Küche?",
        "Ziehst du eine bestimmte Küche vor? (Bsp. italienisch, thai oder regional)",
        "Aus welcher Küche soll das Rezept sein?"],
    # MENU
    "S2.2": ["Was für eine Menu-Art hättest du gerne? (Bsp. Vorspeise, Hauptspeise, Nachtisch)"],
    # DISH TYPE
    "S2.3": ["Gibt es eine bestimmte Art von Gericht, dass du zubereiten möchtest? "
             "(Bsp. Snacks, Eintöpfe, Suppen, Salate)"],
    # "S2.3": ["Wie würdest du dein Essen am liebsten zubereiten?",
    #          "(Bsp.: kochen, backen, braten, dünsten)",
    #          "Gibt es spezielle Art, wie du dein Essen zubereiten möchtest? "
    #          "(Bsp.: kochen, backen, braten, dünsten)"],
    # DIET & HEALTHY
    "S2.4": ["Gibt es spezielle Diäten?",
             "Ziehst du eine bestimmte Ernährungsweise vor?"],
    # INGREDIENTS
    "S2.5": ["Welche Zutaten würdest du gerne verwenden?",
             "Welche Zutaten stehen dir zur Verfügung?",
             # "Was sind deine Lieblingszutaten?",
             "Welche Zutaten möchtest du verwendenden?",
             # "Welches Gemüse magst du?",
             # "Welche Kohlenhydratquelle bevorzugst du normalerweise? "
             # "(Bsp.: Kartoffeln, Nudeln oder Reis)",
             # "Gibt es spezielle Zutaten, die du magst? (Bsp.: Szechuan Pfeffer oder Tamarinde)"
             ],
    "S3.0": ["Suche läuft..."],
    "S3.1.1": ["Deine Präferenzen: PREFERENCES_PLACEHOLDER. ",
               "Du hast erwähnt, dass du folgendes magst: PREFERENCES_PLACEHOLDER."],
    "S3.1": ["Ich hätte schon ein Rezept für dich. Wie klingt 'RECIPE_TITLE_PLACEHOLDER?'",
             "Für deine Präferenzen habe ich folgendes Rezept gefunden: 'RECIPE_TITLE_PLACEHOLDER'. Wie klingt dieses Rezept für dich?",
             "Entsprechend deiner Präferenzen, habe ich folgendes Rezept gefunden 'RECIPE_TITLE_PLACEHOLDER'. Wie klingt das für dich?",
             "Wie klingt 'RECIPE_TITLE_PLACEHOLDER' fuer dich?"],
    "S3.2": ["Möchtest du die Zutatenliste sehen?"],
    "S3.3": ["Wie gefallen dir die Zutaten?",
             "Wie findest du die Zutaten?"],
    "S3.4": ["Möchtest du das Rezept sehen?"],
    "S3.5": ["Wie findest du das Rezept?",
             "Wie gefällt dir das Rezept?"],
    "S3.6": ["Ich habe kein Rezept gefunden, dass deinen Präferenzen entspricht. "
             "Lass uns noch mal probieren. Was würdest du gerne essen?"],
    "S3.7": ["Rezept wurde nicht angenommen, wir probieren ein anderes Rezept."],
    "S3.8": ["Hier sind weitere Details zum Rezept: "],
    "S3.9": ["Hier ist ein Bild von dem Rezept: "],
    "S4.1": ["Bist du sicher, dass du dieses Gespräch beenden möchtest?"],
    "S4.2": ["Ich werde dieses Gespräch beenden. Ich hoffe, ich konnte dir behilflich sein.",
             "Vielen Dank! Bis zum nächsten Mal!"],
    "S4.3": ["Wir machen weiter mit der aktuellen Empfehlung."],
    "S5.1": ["Bist du sicher, dass du deine Präferenzen zurücksetzen möchtest?"],
    "S5.2": ["Ich werde jetzt deine Präferenzen zurücksetzen. Also, was würdest du denn gerne essen?"],
    "S5.3": ["Wir machen weiter mit der aktuellen Empfehlung."],
    "S6.0": ["Du möchtest also eine Alternative."],
    "S0": ["Ich habe leider (noch) keine passende Antwort. Es tut mir leid :)",
           # "Das habe ich nicht verstanden. Könntest du das neu formulieren?",
           # "Das habe ich nicht verstanden. Bitte umformulieren.",
           # "Könntest du das umformulieren? Ich habe deine Eingabe nicht verstanden."
           ],
    "S6": ["System Capabilities Reply"]
}

##############################################
# FEEDBACK/SENTIMENT CLASSIFICATION CONSTANTS:
##############################################

# FEEDBACK_CLASSIFICATION_MODEL_PATH = "C:/Users/emale/anaconda3/envs/conda_ma_env/.guild/runs/afdb0453566e4917ad12054299fa6941/"
FEEDBACK_CLASSIFICATION_MODEL_PATH = "NLU/assets/feedback_classification_model"
FEEDBACK_CLASSIFICATION_MODEL_NAME = "bert-base-german-cased-bert20230209_085147_20230209_085836"

FB_POSITIVE = 0
FB_NEUTRAL = 1
FB_NEGATIVE = 2

FEEDBACK_LABELS_DICTIONARY = {"positive": FB_POSITIVE,
                              "neutral": FB_NEUTRAL,
                              "negative": FB_NEGATIVE}

PADDING_MAX_LEN_SENT = 32
TOKENIZER_FEEDBACK = "bert-base-german-cased"

##################################
# INTENT CLASSIFICATION CONSTANTS:
##################################

PROVIDE_REVISE_PREFERENCES = 0
RESET_PREFERENCES = 1
DISPLAY_INGREDIENTS = 2
DISPLAY_INSTRUCTIONS = 3
DISPLAY_DETAILS = 4
DISPLAY_IMAGES = 5
QUIT = 6
GET_ALTERNATIVES = 7
USER_FEEDBACK = 8
SYS_CAPABILITIES = 9

PLACEHOLDERS_NER = {"ingredients": "ingred_ent",
                    "preparation_method": "prep_ent",
                    "cuisine": "cuisine_ent",
                    "menu": "menu_ent",
                    "occasion": "occasion_ent",
                    "dish_type": "dish_ent",
                    "diet_healthy": "diet_healthy_ent"}

INTENT_LABELS_DICTIONARY = {'01_provide_revise_preferences': PROVIDE_REVISE_PREFERENCES,
                            '02_reset_preferences': RESET_PREFERENCES,
                            '03_display_ingredients': DISPLAY_INGREDIENTS,
                            '04_display_instructions': DISPLAY_INSTRUCTIONS,
                            '05_display_details': DISPLAY_DETAILS,
                            '06_display_image': DISPLAY_IMAGES,
                            '07_quit': QUIT,
                            '08_get_alternatives': GET_ALTERNATIVES,
                            '09_user_feedback': USER_FEEDBACK,
                            '10_system_capabilities': SYS_CAPABILITIES
                            }
PADDING_MAX_LEN_INTENTS = 32
TOKENIZER_INTENT = "bert-base-german-cased"

# INTENT_CLASSIFICATION_MODEL_PATH = "C:/Users/emale/anaconda3/envs/conda_ma_env/.guild/runs/347c849e69ae47918cb0bd37d26c45e7/"
# INTENT_CLASSIFICATION_MODEL_NAME = "german_cased_bert_no_placeholders_20221209_171015_20221209_180422"
#INTENT_CLASSIFICATION_MODEL_PATH = "C:/Users/emale/anaconda3/envs/conda_ma_env/.guild/runs/607f427a3cf74d7697df68a0235438cf/"

INTENT_CLASSIFICATION_MODEL_PATH = "NLU/assets/intent_classification_model"
INTENT_CLASSIFICATION_MODEL_NAME = "german_cased_bert_no_placeholders_20230207_101612_20230207_113053"

######################################
# NER RECIPE TITLE:
######################################

RECIPE_TITLE_ENTITY_REPLACEMENT = "RECIPE_TITLE"
#SPACY_NER_MODEL_PATH = 'C:/Users/emale/Documents/uni/MA/helper_files/jupyter_notebooks/ner-models/complete_data_custom_lr_dropout_output/model-best'
SPACY_NER_MODEL_PATH = 'NLU/assets/ner_recipe_title_model/model-best'

'''
Retrieve the set of stopwords using the following code:

import spacy
import de_core_news_sm
nlp = spacy.load('de_core_news_sm')
# Print the set of spaCy's default stop words (remember that sets are unordered):
print(nlp.Defaults.stop_words)

'''

SPACY_DE_STOPWORDS = ['siebenten', 'damit', 'gekonnt', 'dafür', 'andere', 'schon', 'hier', 'seinem', 'sich', 'richtig',
                      'a', 'magst', 'viel', 'sei', 'fünften', 'sagte', 'dieselben', 'welchen', 'andern', 'einigen',
                      'denselben', 'heute', 'wohl', 'morgen', 'jenes', 'achten', 'weit', 'jedermanns', 'niemandem',
                      'machen', 'gewesen', 'können', 'so', 'sechste', 'sowie', 'tagen', 'dermassen', 'sechs', 'fünftes',
                      'beide', 'welchem', 'siebte', 'zweiter', 'schlecht', 'gekannt', 'dir', 'keinem', 'sollte', 'ab',
                      'in', 'tun', 'zunächst', 'vierte', 'besten', 'besonders', 'keinen', 'demgegenüber', 'weniges',
                      'darüber', 'diesen', 'fünfter', 'siebtes', 'uhr', 'dritter', 'selbst', 'bin', 'habt', 'durften',
                      'wirklich', 'nun', 'wurden', 'gern', 'muss', 'große', 'kommt', 'bald', 'außerdem', 'das',
                      'dieselbe', 'durchaus', 'bisher', 'sechstes', 'vergangenen', 'zehntes', 'dass', 'drei', 'sind',
                      'zu', 'leider', 'deswegen', 'nur', 'wieder', 'bei', 'zehnter', 'kannst', 'dagegen', 'werde',
                      'wollen', 'ihm', 'gab', 'erste', 'wenig', 'infolgedessen', 'dasselbe', 'konnte', 'unser', 'allem',
                      'vergangene', 'solchen', 'uns', 'sollen', 'jedoch', 'jenen', 'gegen', 'solches', 'oben', 'weil',
                      'hinter', 'würden', 'erst', 'geschweige', 'demselben', 'waren', 'derjenige', 'offen', 'jedermann',
                      'je', 'nie', 'hat', 'beim', 'solche', 'kam', 'jener', 'deinem', 'dies', 'wenn', 'manchen', 'du',
                      'wird', 'heisst', 'denn', 'na', 'jemand', 'ebenso', 'ag', 'erster', 'weiter', 'auch', 'ausser',
                      'recht', 'bekannt', 'welcher', 'manches', 'neben', 'noch', 'einander', 'sonst', 'jemanden',
                      'grossen', 'hoch', 'rechten', 'währenddem', 'mich', 'ohne', 'daß', 'jahren', 'jenem', 'besser',
                      'sie', 'kein', 'aus', 'wollt', 'einmal', 'tel', 'meinem', 'ging', 'neunten', 'nach', 'anderen',
                      'der', 'weniger', 'zugleich', 'vier', 'vielleicht', 'ganzes', 'jene', 'gutes', 'danach', 'mit',
                      'achte', 'mein', 'darf', 'etwa', 'tage', 'würde', 'alle', 'ihre', 'daran', 'ihrer', 'hast',
                      'währenddessen', 'kleine', 'darin', 'muß', 'niemand', 'sieben', 'des', 'deren', 'also', 'seine',
                      'zweite', 'ein', 'allen', 'dem', 'daher', 'will', 'wessen', 'einem', 'immer', 'gerade', 'nichts',
                      'dürfen', 'vielem', 'trotzdem', 'bis', 'eigene', 'weitere', 'jahr', 'mehr', 'dahin', 'am',
                      'allgemeinen', 'davor', 'demgemäss', 'außer', 'um', 'dürft', 'siebentes', 'derselbe', 'kann',
                      'satt', 'überhaupt', 'kaum', 'gut', 'teil', 'ersten', 'bereits', 'entweder', 'zum', 'wann',
                      'früher', 'manche', 'musste', 'zwischen', 'während', 'diesem', 'zuerst', 'seiner', 'vor',
                      'damals', 'übrigens', 'weiteres', 'im', 'gesagt', 'mögen', 'dadurch', 'dessen', 'siebenter',
                      'solcher', 'deshalb', 'wäre', 'groß', 'siebten', 'grosse', 'ihn', 'diejenigen', 'mir', 'seid',
                      'gemusst', 'konnten', 'möglich', 'wenige', 'ihres', 'neunter', 'dahinter', 'hatten', 'aller',
                      'weiteren', 'ihr', 'ausserdem', 'keine', 'kommen', 'allein', 'musst', 'als', 'wie', 'ganzen',
                      'kleiner', 'ganz', 'deiner', 'macht', 'wir', 'ende', 'es', 'nicht', 'diese', 'genug', 'gehen',
                      'keiner', 'achtes', 'jede', 'mochte', 'an', 'ihren', 'und', 'dort', 'zurück', 'wo', 'endlich',
                      'seinen', 'statt', 'unter', 'vierter', 'deine', 'zusammen', 'unsere', 'gute', 'zwanzig', 'beiden',
                      'wem', 'eigen', 'dritte', 'lange', 'ich', 'dritten', 'ins', 'mittel', 'darunter', 'welches',
                      'lang', 'kleines', 'los', 'tag', 'her', 'dermaßen', 'vom', 'solang', 'war', 'die', 'gibt',
                      'sechsten', 'dich', 'mögt', 'jetzt', 'euch', 'zeit', 'wahr', 'oft', 'derjenigen', 'erstes',
                      'dein', 'auf', 'elf', 'eines', 'ja', 'mochten', 'nachdem', 'en', 'manchem', 'seines', 'geworden',
                      'grosses', 'machte', 'was', 'fünfte', 'werden', 'wollten', 'anders', 'nein', 'hätte', 'müsst',
                      'eine', 'gleich', 'drin', 'für', 'etwas', 'dasein', 'gross', 'er', 'acht', 'sah', 'könnt',
                      'meinen', 'drittes', 'sein', 'einmaleins', 'jemandem', 'beispiel', 'achter', 'dazu', 'alles',
                      'zur', 'dank', 'wurde', 'rechte', 'unserer', 'wegen', 'vierten', 'sagt', 'ist', 'meines',
                      'demzufolge', 'niemanden', 'rechter', 'dementsprechend', 'hatte', 'zwei', 'ach', 'darauf',
                      'ehrlich', 'solchem', 'meine', 'rund', 'ihnen', 'ob', 'irgend', 'dieses', 'á', 'daneben', 'tat',
                      'daraus', 'sondern', 'eigenes', 'werdet', 'darfst', 'gegenüber', 'sollten', 'zehnten', 'jedem',
                      'haben', 'neun', 'desselben', 'gedurft', 'wenigstens', 'bist', 'lieber', 'anderem', 'darum',
                      'oder', 'kleinen', 'mancher', 'viele', 'gar', 'daselbst', 'diejenige', 'dieser', 'durfte', 'zehn',
                      'davon', 'eben', 'zweites', 'heißt', 'sechster', 'demgemäß', 'natürlich', 'mussten', 'hätten',
                      'einen', 'man', 'neuntes', 'indem', 'seitdem', 'jahre', 'siebter', 'kurz', 'den', 'einige',
                      'eigener', 'fünf', 'zehnte', 'ganze', 'willst', 'neuen', 'von', 'warum', 'wer', 'leicht', 'hin',
                      'eigenen', 'siebente', 'müssen', 'dazwischen', 'jeder', 'könnte', 'über', 'ihrem', 'ganzer',
                      'welche', 'grosser', 'möchte', 'neunte', 'meiner', 'aber', 'einiges', 'habe', 'guter', 'einer',
                      'später', 'gemacht', 'wen', 'denen', 'großes', 'gemocht', 'zwar', 'da', 'wollte', 'dann',
                      'großer', 'durch', 'nahm', 'dabei', 'allerdings', 'derselben', 'gehabt', 'worden', 'neue', 'seit',
                      'wart', 'zweiten', 'mag', 'gewollt', 'vielen', 'einiger', 'geht', 'großen', 'soll', 'rechtes',
                      'wirst', 'jeden', 'seien', 'viertes', 'sehr', 'doch']

#################################
# RECIPE SIMILARITY
#################################

EMBEDDINGS_PICKLE_FILE_NAME = "distiluse-base-multi_embeddings_norm_case_no_stop_no_lemma.pkl"
EMBEDDINGS_PICKLE_FILE_PATH = "NLU/assets/recipe_similarity_embeddings"

NO_TOP_SIMILAR_RECIPES = 1
SIMILARITY_THRESHOLD = 0.8