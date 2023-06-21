import copy
import os
import re

from utils import check_changes_in_preferences, clean_recipe_title, format_preferences_for_display

os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'
import random
# from germansentiment import SentimentModel
import dialogManager.bt as behavior_tree
from NLU.crs_ner import NER
from NLU.crs_intent_classification import IntentClassifier
from NLU.crs_feedback_classification import FeedbackClassifier
from NLU.crs_ner_recipe_title import NERRecipeTile
from NLU.CONSTANTS import STATES_SYSTEM_PROMPTS, PLACEHOLDERS_NER

from Recommender.recipe_recommender import RecipeRecommender

from flask_socketio import emit

"""
    The Manager class receives user input from the flaskApp/routes.py and passes it to the NLU components for
    information extraction. Once the results received, they are gathered in a dictionary passed to the BT to update
    the blackboard with identified data than ticks to check the updated state of the bt. For each state it retrieves the
    corresponding state prompt from the CONSTANTS file.
    
    For each state it also needs to check if any extra actions need to be performed such as search/resets that require an
    additional tick.
    
"""

# mnagerul primeste data de la routes si da mai departe la nlu
# nlu proceseaza si raspunde cu entities si intents
# manageru raspunde la routes trimitand entities si intents, ca sa poata fi arata userului pt debug


class Manager:
    def __init__(self):
        print("Init manager class...")
        self.bt = behavior_tree.create_root()
        self.bt.setup_with_descendants()
        # behavior_tree.tree_stewardship(self.bt)

        self.current_recommendation_index = None
        self.changes_in_preferences = False

        self.ner = NER()
        self.ner_recipe_title = NERRecipeTile()

        self.recommender = RecipeRecommender()

        self.classifier = IntentClassifier()
        self.feedbackClassifier = FeedbackClassifier()
        # self.sentiModel = SentimentModel()

    def process(self, data):
        # GETS THE ENTITIES AND CURRENT INTENT FROM THE RESPECTIVE CLASSES
        # EACH CALL OF THE ner_recognition ALSO RETURNS A STRING WITH PLACEHOLDERS INSTEAD OF THE RECOGNIZED ENTITIES
        # !ORDER IMPORTANT: NEXT CALL GETS THE STRING FROM THE PREVIOUS CALL AND PROCESSES IT FURTHER

        # CHECK FOR CONFLICTS: WHAT IF IN AND OUT LISTS CONTAIN SAME ELEMENT?
        # "Es tut mir leid, das habe ich nicht verstanden. Soll es mit x / x sein?"

        # self.classifier.predict_intent(data['msg'])[0],
        # current_intent = self.classifier.predict_intent(ingredients["input_with_entity_replacement"])
        current_intent = self.classifier.predict_intent(data['msg'])  # 0 is for string

        # as feedback we need the string, e.g. neutral, to pass it to the bt-blackboard
        current_sentiment = self.feedbackClassifier.predict_feedback([data['msg']])[0]

        extracted_entities = {
            "named_entities": {
                "cuisine": self.ner.ner_recognition(data['msg'],
                                                    collection="cuisine",
                                                    field="cuisine",
                                                    replacement=PLACEHOLDERS_NER["cuisine"]),
                "menu_type": self.ner.ner_recognition(data['msg'],
                                                      collection="menu",
                                                      field="menu",
                                                      replacement=PLACEHOLDERS_NER["menu"]),
                "occasion": self.ner.ner_recognition(data['msg'],
                                                     collection="occasion",
                                                     field="occasion",
                                                     replacement=PLACEHOLDERS_NER["occasion"]),
                "preparation": self.ner.ner_recognition(data['msg'],
                                                        collection="preparation_method",
                                                        field="preparation_method",
                                                        replacement=PLACEHOLDERS_NER["preparation_method"]),
                "dish_type": self.ner.ner_recognition(data['msg'],
                                                      collection="dish_type",
                                                      field="dish_type",
                                                      replacement=PLACEHOLDERS_NER["dish_type"]),
                "diet_healthy": self.ner.ner_recognition(data['msg'],
                                                         collection="diet_healthy",
                                                         field="diet_healthy_category",
                                                         replacement=PLACEHOLDERS_NER["diet_healthy"]),
                "ingredients": self.ner.ner_recognition(data['msg'],
                                                        collection="ingredients",
                                                        field="ingredient",
                                                        replacement=PLACEHOLDERS_NER["ingredients"])
            },
            "current_intent": current_intent[1],
            "intent_string": current_intent[0],
            "feedback": current_sentiment
        }

        recipe_title = self.ner_recipe_title.get_recipe_title(data['msg'])
        recipe_title = clean_recipe_title(extracted_entities["named_entities"], recipe_title)

        extracted_entities["named_entities"]["recipe_title"] = recipe_title

        # GET PREVIOUS PREFERENCES FROM THE BT
        old_preferences = copy.deepcopy(behavior_tree.get_blackboard_preferences()["named_entities"])

        # POSSIBLE TO CREATE CONDITION: IF RECIPE TITLE OR DISH TYPE ARE DIFFERENT THAN THE PREVIOUS ONES, DELETE
        # PREFERENCES FROM THE BT-BLACKBOARD
        # A SIMILAR ISSUE IS NOT BEING ABLE TO CHECK FOR CONFLICTS THAT MIGHT ARISE WITHIN MADE PREFERENCES

        if current_intent[1] == 9:
            sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                            "system_prompt": random.choice(STATES_SYSTEM_PROMPTS["S0"])}
            emit('system_prompt', {'system_prompt': sys_response})
            print("Manager\n------------------------------------------ Tick -----------------------------------------\n")
            self.bt.tick_once()


        # UPDATE BT WITH NEW PREFERENCES
        behavior_tree.update_blackboard(extracted_entities)

        if behavior_tree.get_state() in ["S3.1", "S3.2", "S3.3"]:
            # self.changes_in_preferences - boolean
            self.changes_in_preferences = check_changes_in_preferences(old_preferences,
                                                                       behavior_tree.get_blackboard_preferences()[
                                                                           "named_entities"])

        """
        IN CERTAIN STATES [SEARCH FOR RECIPE | RECIPE NOT FOUND | DISPLAY DETAILS | DISPLAY PICTURE] THE SYSTEM [ITS 
        STATE AND PROMPT] MUST BE UPDATED MULTIPLE TIMES BETWEEN CONSECUTIVE USER INPUTS => THEREFORE WE NEED TO 
        CHECK/UPDATE THE SYSTEM STATE AND TICK THE TREE AGAIN
        """

        # CHECK SYSTEM STATE BEFORE UPDATE + UPDATE + CHECK SYSTEM STATE AFTER UPDATE
        state_before_tick = behavior_tree.get_state()
        print("Manager\n------------------------------------------ Tick -----------------------------------------\n")
        self.bt.tick_once()

        # PREPARE AND SEND SYSTEM PROMPT TO GUI
        if behavior_tree.get_state() not in ["S3.1", "S3.3", "S3.5"]:
            sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                            "system_prompt": random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])}
            emit('system_prompt', {'system_prompt': sys_response})
            print("Manager - BB preferences after tick: ", sys_response)

        ################################################################################################################
        # S3.0 => Searching for recipe
        if behavior_tree.get_state() == "S3.0":
            print("Manger - CURRENT STATE S3.0")
            self._search_recommendation()

        ################################################################################################################
        # S3.7 => Recipe not accepted => need to restart search
        if behavior_tree.get_state() == "S3.7":
            print("Manger - CURRENT STATE S3.7")
            print(
                "Manager\n------------------------------------------ Tick -----------------------------------------\n")
            self.bt.tick_once()

            # need to run this again because the system state changed
            sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                            "system_prompt": random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])}
            emit('system_prompt', {'system_prompt': sys_response})

            ############################################################################################################
            # S3.0 => Searching for recipe
            if behavior_tree.get_state() == "S3.0":
                print("Manger - CURRENT STATE S3.0")
                self._search_recommendation()

        ################################################################################################################
        # S6.0 => Get Alternative => need to restart search
        if behavior_tree.get_state() == "S6.0":
            print("Manger - CURRENT STATE S6.0")
            print(
                "Manager\n------------------------------------------ Tick -----------------------------------------\n")
            self.bt.tick_once()

            # need to run this again because the system state changed
            sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                            "system_prompt": random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])}
            emit('system_prompt', {'system_prompt': sys_response})

            ############################################################################################################
            # S3.0 => Searching for recipe
            if behavior_tree.get_state() == "S3.0":
                print("Manger - CURRENT STATE S3.0")
                # self._search_similar_recommendation()
                self._search_recommendation()

        ################################################################################################################
        # S3.3 => Show ingredients
        if behavior_tree.get_state() == "S3.3":
            print("Manger - CURRENT STATE S3.3 - current recc index: ", self.current_recommendation_index)

            prompt = random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])
            prompt_with_ingredients = self.recommender.get_ingredients(self.current_recommendation_index)
            sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                            "system_prompt": prompt,
                            "ingredients": prompt_with_ingredients}
            emit('system_prompt', {'system_prompt': sys_response})

        ################################################################################################################
        # S3.5 => Show instructions
        if behavior_tree.get_state() == "S3.5":
            print("Manger - CURRENT STATE S3.5 - current recc index: ", self.current_recommendation_index)

            prompt = random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])
            prompt_with_instructions = self.recommender.get_instructions(self.current_recommendation_index)
            sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                            "system_prompt": prompt,
                            "instructions": prompt_with_instructions}
            emit('system_prompt', {'system_prompt': sys_response})

        ################################################################################################################
        # S3.8 / S3.9 => Display details / Display picture
        if behavior_tree.get_state() in ["S3.8", "S3.9"]:
            print("Manger - CURRENT STATE S3.8/S3.9")

            prompt_with_extras = ""
            if behavior_tree.get_state() == "S3.8":
                prompt_with_extras = self.recommender.get_details(self.current_recommendation_index)
                sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                                "details": prompt_with_extras}
                emit('system_prompt', {'system_prompt': sys_response})
            else:
                prompt_with_extras = self.recommender.get_img_href(self.current_recommendation_index)
                sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                                "img_href": prompt_with_extras}
                emit('system_prompt', {'system_prompt': sys_response})
            print(
                "Manager\n------------------------------------------ Tick -----------------------------------------\n")
            self.bt.tick_once()

            ############################################################################################################
            # S3.1 => Recipe found
            if behavior_tree.get_state() == "S3.1":
                print("Manger - CURRENT STATE S3.1 - current recc index: ", self.current_recommendation_index)

                prompt_with_title = random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])
                prompt_with_title = prompt_with_title.replace("RECIPE_TITLE_PLACEHOLDER", self.recommender.get_title(
                    self.current_recommendation_index))

                print("Manger - CURRENT STATE S3.1 - current prompt with title: ", prompt_with_title)

                sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                                "system_prompt": prompt_with_title}
                emit('system_prompt', {'system_prompt': sys_response})

            ############################################################################################################
            # S3.3 => Show ingredients
            if behavior_tree.get_state() == "S3.3":
                print("Manger - CURRENT STATE S3.3 - current recc index: ", self.current_recommendation_index)

                # prompt = random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])
                # prompt_with_ingredients = self.recommender.get_ingredients(self.current_recommendation_index)
                # sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                #                "system_prompt": prompt,
                #                "ingredients": prompt_with_ingredients}
                # emit('system_prompt', {'system_prompt': sys_response})

                prompt = random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])
                sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                                "system_prompt": prompt}
                emit('system_prompt', {'system_prompt': sys_response})

            ############################################################################################################
            # S3.5 => Show instructions
            if behavior_tree.get_state() == "S3.5":
                print("Manger - CURRENT STATE S3.5 - current recc index: ", self.current_recommendation_index)

                # prompt_with_instructions = self.recommender.get_instructions(self.current_recommendation_index)
                # sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                #                "system_prompt": prompt_with_instructions}
                # emit('system_prompt', {'system_prompt': sys_response})

                prompt = random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])
                sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                                "system_prompt": prompt}
                emit('system_prompt', {'system_prompt': sys_response})

        ################################################################################################################
        # S4.3 / S5.3 => Reset Preferences Not Confirmed
        if behavior_tree.get_state() in ["S4.3", "S5.3"]:
            print("Manger - CURRENT STATE S4.3/S5.3")
            print(
                "Manager\n------------------------------------------ Tick -----------------------------------------\n")
            self.bt.tick_once()
            print("Manger - CURRENT STATE S4.3/S5.3 => state after tick: ", behavior_tree.get_state())
            ############################################################################################################
            # S3.1 => Recipe found
            if behavior_tree.get_state() == "S3.1":
                print("Manger - CURRENT STATE S3.1 [inside S4.3/S5.3] - current recc index: ",
                      self.current_recommendation_index)

                prompt_with_title = random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])
                prompt_with_title = prompt_with_title.replace("RECIPE_TITLE_PLACEHOLDER", self.recommender.get_title(
                    self.current_recommendation_index))

                sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                                "system_prompt": prompt_with_title}
                emit('system_prompt', {'system_prompt': sys_response})

            ############################################################################################################
            # S3.3 => Show ingredients
            elif behavior_tree.get_state() == "S3.3":
                print("Manger - CURRENT STATE S3.3 - current recc index: ", self.current_recommendation_index)

                # prompt = random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])
                # prompt_with_ingredients = self.recommender.get_ingredients(self.current_recommendation_index)
                # sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                #                "system_prompt": prompt,
                #                "ingredients": prompt_with_ingredients}
                # emit('system_prompt', {'system_prompt': sys_response})

                prompt = random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])
                sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                                "system_prompt": prompt}
                emit('system_prompt', {'system_prompt': sys_response})

            ############################################################################################################
            # S3.5 => Show instructions
            elif behavior_tree.get_state() == "S3.5":
                print("Manger - CURRENT STATE S3.5 - current recc index: ", self.current_recommendation_index)

                # prompt_with_instructions = self.recommender.get_instructions(self.current_recommendation_index)
                # sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                #                "system_prompt": prompt_with_instructions}
                # emit('system_prompt', {'system_prompt': sys_response})

                prompt = random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])
                sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                                "system_prompt": prompt}
                emit('system_prompt', {'system_prompt': sys_response})

            ############################################################################################################
            # any other state that might occur
            else:
                sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                                "system_prompt": random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])}
                emit('system_prompt', {'system_prompt': sys_response})
                print("Manager - BB preferences after tick: ", sys_response)

        ################################################################################################################
        # S4.2 => QUIT
        if behavior_tree.get_state() == "S4.2":
            print("Manger - CURRENT STATE S4.2 - QUIT")
            # sys_response["end_conversation"] = 1
            emit('end', {})

    def _search_recommendation(self):
        # SEARCH INCLUDES QUERY DB + DISPLAY TITLE TO USER + DEAL WITH NO SEARCH RESULT
        # recommendation <=> recipe title

        # display preferences we have recognized and which will be considered in the search
        sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                        "entities": format_preferences_for_display(
                            behavior_tree.get_blackboard_preferences()["named_entities"])}
        emit('system_prompt', {'system_prompt': sys_response})

        # retrieve recipe recommendation index
        self.current_recommendation_index = self.recommender.get_recommendation(
            behavior_tree.get_blackboard_preferences()["named_entities"])
        print("manager - recommendation", self.current_recommendation_index)
        behavior_tree.update_blackboard({"search_completed": True})

        # if no recipe found, the index is None => after tick the bt will reach recipe not found (S3.6) => preferences
        # will be reset and conversation restarted
        if self.current_recommendation_index is None:
            print("recommendation is none", self.current_recommendation_index)
            behavior_tree.update_blackboard({"recommendation_found": False})
        # the bt is ticked again and will reach S3.1, see next if statement
        else:
            print("recommendation found", self.current_recommendation_index)
            behavior_tree.update_blackboard({"recommendation_found": True})

        print("Manager\n------------------------------------------ Tick -----------------------------------------\n")
        self.bt.tick_once()

        ########################################################################################################
        # S3.1 => Recipe found
        if behavior_tree.get_state() == "S3.1":
            print("Manger - CURRENT STATE S3.0 => S3.1 - current recc index: ", self.current_recommendation_index)

            # we retrieve the recipe title based on the id and use it to replace the placeholder in the system prompt
            prompt_with_title = random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])
            prompt_with_title = prompt_with_title.replace("RECIPE_TITLE_PLACEHOLDER", self.recommender.get_title(
                self.current_recommendation_index))
            print("Manger - CURRENT STATE S3.1 - current prompt with title: ", prompt_with_title)

            sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                            "system_prompt": prompt_with_title}
            emit('system_prompt', {'system_prompt': sys_response})

        ###########################################################################################################
        # S3.6 => No recipe found
        if behavior_tree.get_state() == "S3.6":
            print("Manger - CURRENT STATE S3.6")

            behavior_tree.update_blackboard({"search_completed": False})
            behavior_tree.update_blackboard({"recommendation_found": False})

            sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                            "system_prompt": random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])}
            emit('system_prompt', {'system_prompt': sys_response})

            print(
                "Manager\n------------------------------------------ Tick -----------------------------------------\n")
            self.bt.tick_once()

    def _search_similar_recommendation(self):
        sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                        "entities": format_preferences_for_display(
                            behavior_tree.get_blackboard_preferences()["named_entities"])}
        emit('system_prompt', {'system_prompt': sys_response})

        if self.changes_in_preferences:
            self.current_recommendation_index = self.recommender.get_recommendation(
                behavior_tree.get_blackboard_preferences()["named_entities"])
            print("manager - recommendation", self.current_recommendation_index)
            behavior_tree.update_blackboard({"search_completed": True})

            # if no recipe found, the index is None => after tick the bt will reach recipe not found (S3.6) => preferences
            # will be reset and conversation restarted
            if self.current_recommendation_index is None:
                print("recommendation is none", self.current_recommendation_index)
                behavior_tree.update_blackboard({"recommendation_found": False})
            # the bt is ticked again and will reach S3.1, see next if statement
            else:
                print("recommendation found", self.current_recommendation_index)
                behavior_tree.update_blackboard({"recommendation_found": True})

            print(
                "Manager\n------------------------------------------ Tick -----------------------------------------\n")
            self.bt.tick_once()

        else:
            print("Manager S6.0 - Preferences DID NOT change! Search for similar recipe")
            similar_to_index = self.current_recommendation_index
            similar_recipes_list = self.recommender.get_similar_recipes(similar_to_index)

            if similar_recipes_list:
                print("++++++++++++++++++++++++++++++++++++")
                print("Manager - similar recipes: ", len(similar_recipes_list), similar_recipes_list)
                print("++++++++++++++++++++++++++++++++++++")
                self.current_recommendation_index = random.choice(similar_recipes_list)
                print("Random ID: ", self.current_recommendation_index)
                self.recommender.add_index_to_history(self.current_recommendation_index)

            print("manager - recommendation", self.current_recommendation_index)
            behavior_tree.update_blackboard({"search_completed": True})

            if self.current_recommendation_index is None:
                print("recommendation is none", self.current_recommendation_index)
                behavior_tree.update_blackboard({"recommendation_found": False})
            else:
                print("recommendation found", self.current_recommendation_index)
                behavior_tree.update_blackboard({"recommendation_found": True})

            print("Manager\n------------------------------------------ Tick -----------------------------------------\n")
            self.bt.tick_once()

        ########################################################################################################
        # S3.1 => Recipe found
        if behavior_tree.get_state() == "S3.1":
            print("Manger - CURRENT STATE S3.0 => S3.1 - current recc index: ", self.current_recommendation_index)

            prompt_with_title = random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])
            prompt_with_title = prompt_with_title.replace("RECIPE_TITLE_PLACEHOLDER", self.recommender.get_title(
                self.current_recommendation_index))
            print("Manger - CURRENT STATE S3.1 - current prompt with title: ", prompt_with_title)

            sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                            "system_prompt": prompt_with_title}
            emit('system_prompt', {'system_prompt': sys_response})

        ###########################################################################################################
        # S3.6 => No recipe found
        if behavior_tree.get_state() == "S3.6":
            print("Manger - CURRENT STATE S3.6")

            behavior_tree.update_blackboard({"search_completed": True})
            behavior_tree.update_blackboard({"recommendation_found": False})

            sys_response = {"bb_vars": behavior_tree.get_blackboard_preferences(),
                            "system_prompt": random.choice(STATES_SYSTEM_PROMPTS[behavior_tree.get_state()])}
            emit('system_prompt', {'system_prompt': sys_response})

            print(
                "Manager\n------------------------------------------ Tick -----------------------------------------\n")
            self.bt.tick_once()
