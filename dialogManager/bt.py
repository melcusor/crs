#!/usr/bin/env python
#
#   License: BSD
#   https://raw.githubusercontent.com/splintered-reality/py_trees/devel/LICENSE
#
##############################################################################
# Imports
##############################################################################
import sys
import py_trees
import operator
import random

from NLU import CONSTANTS as C

INTENTS_NAMESPACE = "/intents/"
BB_KEY_CURRENT_INTENT = "current_intent"
BB_KEY_PREVIOUS_INTENT = "previous_intent"
BB_KEY_FEEDBACK = "feedback"  # one of: positive, negative, neutral

RECIPE_PARAM_NAMESPACE = "/recipe_parameters/"
BB_KEY_RECIPE_TITLE_IN = "recipe_title_in"
BB_KEY_RECIPE_TITLE_OUT = "recipe_title_out"

BB_KEY_CUISINE_IN = "cuisine_in"
BB_KEY_CUISINE_OUT = "cuisine_out"

BB_KEY_MENU_TYPE_IN = "menu_type_in"
BB_KEY_MENU_TYPE_OUT = "menu_type_out"

BB_KEY_INGREDIENTS_IN = "ingredients_in"
BB_KEY_INGREDIENTS_OUT = "ingredients_out"

BB_KEY_PREPARATION_IN = "preparation_in"
BB_KEY_PREPARATION_OUT = "preparation_out"

BB_KEY_OCCASION_IN = "occasion_in"
BB_KEY_OCCASION_OUT = "occasion_out"

BB_KEY_DISH_TYPE_IN = "dish_type_in"
BB_KEY_DISH_TYPE_OUT = "dish_type_out"

BB_KEY_DIET_IN = "diet_healthy_in"
BB_KEY_DIET_OUT = "diet_healthy_out"

BB_KEY_ENOUGH_PREFERENCES = "enough_preferences"
# BB_KEY_SERVINGS = "servings"
# BB_KEY_COOKING_TIME = "cooking_time"

# the found_check key os a Boolean
RECOMMENDATION_NAMESPACE = "/recommendation_params/"
BB_KEY_REC_FOUND_CHECK = "recommendation_found"
BB_KEY_REC_LIST = "recommendation_list"
# current recommendation key might be a dictionary
BB_KEY_CURRENT_REC = "current_recommendation"

DISPLAY_PARAM_NAMESPACE = "/display_params/"
BB_KEY_DISPLAY_TITLE = "display_title"  # which component should be displayed
BB_KEY_TITLE_DISPLAYED_CHECK = "title_displayed"  # bool if title of current recommendation already displayed
# BB_KEY_TITLE_ACCEPT_CHECK = "title_accepted"

# BB_KEY_SKIP_INGREDIENTS_CHECK = "skip_ingredients"
BB_KEY_DISPLAY_INGREDIENTS = "display_ingredients"  # which component should be displayed
BB_KEY_INGREDIENTS_DISPLAYED_CHECK = "ingredients_displayed"  # bool if ingredients of current rec. already displayed
# BB_KEY_INGREDIENTS_ACCEPTED_CHECK = "ingredients_accepted"

BB_KEY_DISPLAY_INSTRUCTIONS = "display_instructions"  # which component should be displayed
BB_KEY_INSTRUCTIONS_DISPLAYED_CHECK = "instructions_displayed"  # bool if instructions of current recommendation already displayed
# BB_KEY_REC_ACCEPTED_CHECK = "recipe_accepted"

BB_KEY_SEARCH_COMPLETED_CHECK = "search_completed"
BB_KEY_CURRENT_SYSTEM_STATE = "current_system_state"
BB_KEY_PREVIOUS_SYSTEM_STATE = "previous_system_state"
# BB_KEY_CONFIRM_QUIT = "confirm_quit"
# BB_KEY_CONFIRM_RESET_PREFERENCES = "confirm_reset_preferences"
# BB_KEY_PROCESS_INTERRUPT = "process_interrupt"

BB_SLASH = "/"


##############################################################################
# Classes
#############################################################################
class EnterIngredientValue(py_trees.behaviour.Behaviour):
    def __init__(self, name="EnterIngredientValue"):
        """Configure the name of the behaviour."""
        super(EnterIngredientValue, self).__init__(name)
        self.logger.debug("%s.__init__()" % self.__class__.__name__)

        self.enterIngredientValueBBClient = self.attach_blackboard_client(name="enterIngredientValueBBClient")
        self.enterIngredientValueBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                       access=py_trees.common.Access.WRITE)
        self.enterIngredientValueBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                       access=py_trees.common.Access.WRITE)

    def setup(self):
        """No delayed initialisation required for this example."""
        self.logger.debug("%s.setup()" % self.__class__.__name__)

    def initialise(self):
        """
        Reset a counter variable.
        """
        self.logger.debug("%s.initialise()" % self.__class__.__name__)

    def update(self):
        """Increment the counter and decide on a new status."""
        new_status = py_trees.common.Status.RUNNING
        self.enterIngredientValueBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                              self.enterIngredientValueBBClient.get(
                                                  BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE))
        self.enterIngredientValueBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S2.5")

        return new_status

    def terminate(self, new_status):
        """
        Nothing to clean up in this example.
        """
        self.logger.debug("%s.terminate()[%s->%s]" % (self.__class__.__name__, self.status, new_status))


class EnterFurtherPreference(py_trees.behaviour.Behaviour):
    def __init__(self, name="EnterFurtherPreference"):
        """Configure the name of the behaviour."""
        super(EnterFurtherPreference, self).__init__(name)
        self.logger.debug("%s.__init__()" % self.__class__.__name__)

        self.preference_options = [BB_KEY_CUISINE_IN, BB_KEY_MENU_TYPE_IN, BB_KEY_DISH_TYPE_IN, BB_KEY_DIET_IN]

        self.enterContextValueBBClient = self.attach_blackboard_client(name="enterContextValueWA")

        self.enterContextValueBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_IN,
                                                    access=py_trees.common.Access.WRITE)
        self.enterContextValueBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_IN,
                                                    access=py_trees.common.Access.WRITE)
        self.enterContextValueBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_IN,
                                                    access=py_trees.common.Access.WRITE)
        self.enterContextValueBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_IN,
                                                    access=py_trees.common.Access.WRITE)

        self.enterContextValueBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                    access=py_trees.common.Access.WRITE)
        self.enterContextValueBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                    access=py_trees.common.Access.WRITE)

    def setup(self):
        """No delayed initialisation required for this example."""
        self.logger.debug("%s.setup()" % self.__class__.__name__)

    def initialise(self):
        """
        Reset a counter variable.
        """

        self.logger.debug("%s.initialise()" % self.__class__.__name__)

    def update(self):
        """Increment the counter and decide on a new status."""
        print("Update in EnterFurtherPreference")
        print("Left preference options: ", self.preference_options)
        # has to be running, to allow coming back when recipe component not accepted
        new_status = py_trees.common.Status.RUNNING
        self.enterContextValueBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                           self.enterContextValueBBClient.get(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE))

        if self.preference_options:
            furtherPreference = random.choice(self.preference_options)
            self.preference_options.remove(furtherPreference)
            if len(self.enterContextValueBBClient.get(RECIPE_PARAM_NAMESPACE + furtherPreference)) == 0:

                if furtherPreference == BB_KEY_CUISINE_IN:
                    self.enterContextValueBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S2.1")
                    print("enterContextValues, cuisine")
                if furtherPreference == BB_KEY_MENU_TYPE_IN:
                    self.enterContextValueBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S2.2")
                    print("enterContextValues, menu")
                if furtherPreference == BB_KEY_DISH_TYPE_IN:
                    self.enterContextValueBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S2.3")
                    print("enterContextValues, dish_type_in")
                if furtherPreference == BB_KEY_DIET_IN:
                    self.enterContextValueBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S2.4")
                    print("enterContextValues, diet")
        self.feedback_message = "previous_system_state: " + str(
            self.enterContextValueBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE))
        self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                       new_status, self.feedback_message))

        return new_status

    def terminate(self, new_status):
        """
        Nothing to clean up in this example.
        """
        self.logger.debug("%s.terminate()[%s->%s]" % (self.__class__.__name__, self.status, new_status))


class FindRecipeRecommendation(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        """Configure the name of the behaviour."""
        super(FindRecipeRecommendation, self).__init__(name)
        self.logger.debug("%s.__init__()" % self.__class__.__name__)

        self.findRecipeRecommendationBBClient = self.attach_blackboard_client(name="findRecipeRecommendation")
        self.findRecipeRecommendationBBClient.register_key(key=BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK,
                                                           access=py_trees.common.Access.WRITE)
        self.findRecipeRecommendationBBClient.register_key(key=RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK,
                                                           access=py_trees.common.Access.WRITE)

        self.findRecipeRecommendationBBClient.register_key(key=BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                           access=py_trees.common.Access.WRITE)
        self.findRecipeRecommendationBBClient.register_key(key=BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                           access=py_trees.common.Access.WRITE)

        self.findRecipeRecommendationBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_IN,
                                                           access=py_trees.common.Access.READ)
        self.findRecipeRecommendationBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_OUT,
                                                           access=py_trees.common.Access.READ)

    def setup(self):
        """No delayed initialisation required for this example."""
        self.logger.debug("%s.setup()" % self.__class__.__name__)

    def initialise(self):
        """Reset a counter variable."""
        self.logger.debug("  %s [FindRecipeRecommendation::initialise()]" % self.name)

    def update(self):
        """Increment the counter and decide on a new status."""
        self.findRecipeRecommendationBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                  self.findRecipeRecommendationBBClient.get(
                                                      BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE))
        self.findRecipeRecommendationBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S3.0")

        print("FindRecipeRecommendation - recommendation found: ",
              self.findRecipeRecommendationBBClient.get(RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK))
        print("FindRecipeRecommendation - search completed: ",
              self.findRecipeRecommendationBBClient.get(BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK))

        new_status = py_trees.common.Status.RUNNING

        self.feedback_message = "previous_system_state: " + str(
            self.findRecipeRecommendationBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE))
        self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                       new_status, self.feedback_message))

        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""
        self.logger.debug("%s.terminate()[%s->%s]" % (self.__class__.__name__, self.status, new_status))


class DisplayRecommendationComponent(py_trees.behaviour.Behaviour):
    def __init__(self, name="DisplayRecommendationComponent", display_component=""):
        """Configure the name of the behaviour."""
        super(DisplayRecommendationComponent, self).__init__(name)
        self.logger.debug("%s.__init__()" % self.__class__.__name__)

        self.display_component = display_component
        self.displayRecommendationComponentBBClient = self.attach_blackboard_client(
            name="displayRecommendationComponentWA")
        self.displayRecommendationComponentBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                                 access=py_trees.common.Access.WRITE)
        self.displayRecommendationComponentBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                                 access=py_trees.common.Access.WRITE)
        self.displayRecommendationComponentBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                                 access=py_trees.common.Access.WRITE)
        self.displayRecommendationComponentBBClient.register_key(DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_DISPLAYED_CHECK,
                                                                 access=py_trees.common.Access.WRITE)
        self.displayRecommendationComponentBBClient.register_key(
            DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_DISPLAYED_CHECK,
            access=py_trees.common.Access.WRITE)

    def setup(self):
        """No delayed initialisation required for this example."""
        self.logger.debug("%s.setup()" % self.__class__.__name__)

    def initialise(self):
        """
        Reset a counter variable.
        """
        self.logger.debug("%s.initialise()" % self.__class__.__name__)

    def update(self):
        """Increment the counter and decide on a new status."""
        # This has to be running, to allow returning to the search BT when component not accepted
        new_status = py_trees.common.Status.RUNNING

        self.displayRecommendationComponentBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                        self.displayRecommendationComponentBBClient.get(
                                                            BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE))

        if self.display_component == BB_KEY_DISPLAY_TITLE:
            self.displayRecommendationComponentBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S3.1")
            self.displayRecommendationComponentBBClient.set(
                DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_DISPLAYED_CHECK, True)
            self.feedback_message = "BB_KEY_TITLE_DISPLAYED_CHECK == True"
            self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                           new_status, self.feedback_message))
        elif self.display_component == BB_KEY_DISPLAY_INGREDIENTS:
            self.displayRecommendationComponentBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S3.3")
            self.displayRecommendationComponentBBClient.set(
                DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_DISPLAYED_CHECK, True)
            self.feedback_message = "ingredients_accepted"
            self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                           new_status, self.feedback_message))
        elif self.display_component == BB_KEY_DISPLAY_INSTRUCTIONS:
            self.displayRecommendationComponentBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S3.5")
            self.feedback_message = "instructions_accepted"
            self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                           new_status, self.feedback_message))
        elif self.display_component == "display_details":
            self.displayRecommendationComponentBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S3.8")
            self.feedback_message = "display_details"
            self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                           new_status, self.feedback_message))
        elif self.display_component == "display_images":
            self.displayRecommendationComponentBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S3.9")
            self.feedback_message = "display_images"
            self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                           new_status, self.feedback_message))
        else:
            self.displayRecommendationComponentBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S3.5")
            self.feedback_message = "anything else - here recipe instructions"
            self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                           new_status, self.feedback_message))

        self.feedback_message = "previous_system_state: " + str(
            self.displayRecommendationComponentBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE))
        self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                       new_status, self.feedback_message))
        return new_status

    def terminate(self, new_status):
        """
        Nothing to clean up in this example.
        """
        self.logger.debug("%s.terminate()[%s->%s]" % (self.__class__.__name__, self.status, new_status))


class ConfirmEndConversation(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        """Configure the name of the behaviour."""
        super(ConfirmEndConversation, self).__init__(name)
        self.logger.debug("%s.__init__()" % self.__class__.__name__)

        self.confirmEndConversationBBClient = self.attach_blackboard_client(name="endConversation")

        self.confirmEndConversationBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                         access=py_trees.common.Access.WRITE)
        self.confirmEndConversationBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                         access=py_trees.common.Access.WRITE)

    def setup(self):
        """No delayed initialisation required for this example."""
        self.logger.debug("  %s [EndConversation::setup()]" % self.name)

    def initialise(self):
        """Reset a counter variable."""
        self.logger.debug("  %s [EndConversation::initialise()]" % self.name)

    def update(self):
        """Increment the counter and decide on a new status."""
        # print("BB in in EndConversation: ")
        self.confirmEndConversationBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                self.confirmEndConversationBBClient.get(
                                                    BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE))
        self.confirmEndConversationBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S4.1")
        new_status = py_trees.common.Status.RUNNING

        self.feedback_message = "previous_system_state: " + str(
            self.confirmEndConversationBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE))
        self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status, new_status,
                                                       self.feedback_message))
        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""
        self.logger.debug(
            " %s [EndConversation::terminate().terminate()][%s->%s]" % (self.name, self.status, new_status))


class EndConversation(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        """Configure the name of the behaviour."""
        super(EndConversation, self).__init__(name)
        self.logger.debug("%s.__init__()" % self.__class__.__name__)

        self.endConversationBBClient = self.attach_blackboard_client(name="endConversation")
        self.endConversationBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                  access=py_trees.common.Access.WRITE)
        self.endConversationBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                  access=py_trees.common.Access.WRITE)

    def setup(self):
        """No delayed initialisation required for this example."""
        self.logger.debug("  %s [EndConversation::setup()]" % self.name)

    def initialise(self):
        """Reset a counter variable."""
        self.logger.debug("  %s [EndConversation::initialise()]" % self.name)

    def update(self):
        """Increment the counter and decide on a new status."""
        # print("BB in in EndConversation: ")

        # _reset_blackboard()
        _reset_preferences()
        _reset_search_params()
        _reset_intent_info()
        _reset_state_info()

        self.endConversationBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                         self.endConversationBBClient.get(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE))
        self.endConversationBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S4.2")
        new_status = py_trees.common.Status.SUCCESS

        self.feedback_message = "previous_system_state: " + str(
            self.endConversationBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE))
        self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                       new_status, self.feedback_message))

        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""
        self.logger.debug(" %s [EndConversation::terminate().terminate()][%s->%s]" % (self.name, self.status,
                                                                                      new_status))


class ConfirmResetPreferences(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        """Configure the name of the behaviour."""
        super(ConfirmResetPreferences, self).__init__(name)
        self.logger.debug("%s.__init__()" % self.__class__.__name__)

        self.confirmResetPreferencesBBClient = self.attach_blackboard_client(name="confirmResetPreferences")

        self.confirmResetPreferencesBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                          access=py_trees.common.Access.WRITE)
        self.confirmResetPreferencesBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                          access=py_trees.common.Access.WRITE)

    def setup(self):
        """No delayed initialisation required for this example."""
        self.logger.debug("  %s [ConfirmResetPreferences::setup()]" % self.name)

    def initialise(self):
        """Reset a counter variable."""
        self.logger.debug("  %s [ConfirmResetPreferences::initialise()]" % self.name)

    def update(self):
        """Increment the counter and decide on a new status."""
        self.confirmResetPreferencesBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                 self.confirmResetPreferencesBBClient.get(
                                                     BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE))
        self.confirmResetPreferencesBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S5.1")
        new_status = py_trees.common.Status.RUNNING

        self.feedback_message = "previous_system_state: " + str(
            self.confirmResetPreferencesBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE))
        self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status, new_status,
                                                       self.feedback_message))

        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""
        self.logger.debug(
            " %s [ConfirmResetPreferences::terminate().terminate()][%s->%s]" % (self.name, self.status, new_status))


class ResetPreferences(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        """Configure the name of the behaviour."""
        super(ResetPreferences, self).__init__(name)

        self.logger.debug("%s.__init__()" % self.__class__.__name__)

        self.resetPreferencesBBClient = self.attach_blackboard_client(name="resetPreferences")

        self.resetPreferencesBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                   access=py_trees.common.Access.WRITE)
        self.resetPreferencesBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                   access=py_trees.common.Access.WRITE)

    def setup(self):
        """No delayed initialisation required for this example."""

        self.logger.debug("  %s [ResetPreferences::setup()]" % self.name)

    def initialise(self):
        """Reset a counter variable."""
        self.logger.debug("  %s [ResetPreferences::initialise()]" % self.name)

    def update(self):
        """Increment the counter and decide on a new status."""

        _reset_preferences()
        _reset_search_params()
        _reset_intent_info()
        # _reset_state_info()

        self.resetPreferencesBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                          self.resetPreferencesBBClient.get(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE))

        self.resetPreferencesBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S5.2")

        new_status = py_trees.common.Status.SUCCESS
        self.feedback_message = "previous_system_state: " + str(
            self.resetPreferencesBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE))
        self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                       new_status, self.feedback_message))

        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""

        self.logger.debug(" %s [ResetPreferences::terminate().terminate()][%s->%s]" % (self.name, self.status,
                                                                                       new_status))


class EndNotConfirmed(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        """Configure the name of the behaviour."""
        super(EndNotConfirmed, self).__init__(name)
        self.logger.debug("%s.__init__()" % self.__class__.__name__)

        self.endNotConfirmedBBClient = self.attach_blackboard_client(name="endNotConfirmedBBClient")

        self.endNotConfirmedBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                  access=py_trees.common.Access.WRITE)
        self.endNotConfirmedBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                  access=py_trees.common.Access.WRITE)

    def setup(self):
        """No delayed initialisation required for this example."""

        self.logger.debug("  %s [EndNotConfirmed::setup()]" % self.name)

    def initialise(self):
        """Reset a counter variable."""
        self.logger.debug("  %s [EndNotConfirmed::initialise()]" % self.name)

    def update(self):
        """Increment the counter and decide on a new status."""
        prev_prev_state = self.endNotConfirmedBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE)

        self.endNotConfirmedBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE, prev_prev_state)
        self.endNotConfirmedBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S4.3")
        new_status = py_trees.common.Status.FAILURE

        self.feedback_message = "previous_system_state: " + str(
            self.endNotConfirmedBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE))
        self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                       new_status, self.feedback_message))

        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""

        self.logger.debug(" %s [EndNotConfirmed::terminate().terminate()][%s->%s]" % (self.name, self.status,
                                                                                      new_status))


class ResetNotConfirmed(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        """Configure the name of the behaviour."""
        super(ResetNotConfirmed, self).__init__(name)
        self.logger.debug("%s.__init__()" % self.__class__.__name__)

        self.resetNotConfirmedBBClient = self.attach_blackboard_client(name="resetNotConfirmedBBClient")
        self.resetNotConfirmedBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                    access=py_trees.common.Access.WRITE)
        self.resetNotConfirmedBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                    access=py_trees.common.Access.WRITE)

    def setup(self):
        """No delayed initialisation required for this example."""

        self.logger.debug("  %s [ResetNotConfirmed::setup()]" % self.name)

    def initialise(self):
        """Reset a counter variable."""
        self.logger.debug("  %s [ResetNotConfirmed::initialise()]" % self.name)

    def update(self):
        """Increment the counter and decide on a new status."""
        # print("BB in in EndNotConfirmed: ")

        prev_prev_state = self.resetNotConfirmedBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE)
        # previous_state = self.resetNotConfirmedBBClient.get(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE)

        self.resetNotConfirmedBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE, prev_prev_state)
        self.resetNotConfirmedBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S5.3")

        new_status = py_trees.common.Status.SUCCESS
        # new_status = py_trees.common.Status.FAILURE

        self.feedback_message = "previous_system_state: " + str(
            self.resetNotConfirmedBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE)) + "| pprev: " + str(
            prev_prev_state)
        self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                       new_status, self.feedback_message))

        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""

        self.logger.debug(" %s [ResetNotConfirmed::terminate().terminate()][%s->%s]" % (self.name, self.status,
                                                                                        new_status))


class NoRecipeFound(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        """Configure the name of the behaviour."""
        super(NoRecipeFound, self).__init__(name)
        self.logger.debug("%s.__init__()" % self.__class__.__name__)

        self.noRecipeFoundBBClient = self.attach_blackboard_client(name="noRecipeFoundBBClient")
        self.noRecipeFoundBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                access=py_trees.common.Access.WRITE)
        self.noRecipeFoundBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                access=py_trees.common.Access.WRITE)
        self.noRecipeFoundBBClient.register_key(key=BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK,
                                                access=py_trees.common.Access.WRITE)
        self.noRecipeFoundBBClient.register_key(key=RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK,
                                                access=py_trees.common.Access.WRITE)

    def setup(self):
        """No delayed initialisation required for this example."""

        self.logger.debug("  %s [NoRecipeFound::setup()]" % self.name)

    def initialise(self):
        """Reset a counter variable."""
        self.logger.debug("  %s [NoRecipeFound::initialise()]" % self.name)

    def update(self):
        """Increment the counter and decide on a new status."""
        # print("BB in in EndNotConfirmed: ")
        self.noRecipeFoundBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                       self.noRecipeFoundBBClient.get(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE))
        self.noRecipeFoundBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S3.6")
        self.noRecipeFoundBBClient.set(BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK, True)
        self.noRecipeFoundBBClient.set(RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK, False)

        _reset_preferences()
        _reset_search_params()
        # _reset_intent_info()
        # _reset_state_info()

        self.noRecipeFoundBBClient.set(BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK, True)
        self.noRecipeFoundBBClient.set(RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK, False)

        new_status = py_trees.common.Status.SUCCESS
        self.feedback_message = "previous_system_state: " + str(
            self.noRecipeFoundBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE))
        self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                       new_status, self.feedback_message))

        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""

        self.logger.debug(" %s [ResetNotConfirmed::terminate().terminate()][%s->%s]" % (self.name, self.status,
                                                                                        new_status))


class RecipeComponentNotAccepted(py_trees.behaviour.Behaviour):
    def __init__(self, name, parameter):
        """Configure the name of the behaviour."""
        super(RecipeComponentNotAccepted, self).__init__(name)
        self.logger.debug("%s.__init__()" % self.__class__.__name__)
        self.parameter = parameter
        print("RecipeComponentNotAccepted - parameter: ", self.parameter)

        self.recipeComponentNotAcceptedBBClient = self.attach_blackboard_client(
            name="recipeComponentNotAcceptedBBClient")
        self.recipeComponentNotAcceptedBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                             access=py_trees.common.Access.WRITE)
        self.recipeComponentNotAcceptedBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                             access=py_trees.common.Access.WRITE)
        self.recipeComponentNotAcceptedBBClient.register_key(BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK,
                                                             access=py_trees.common.Access.WRITE)
        self.recipeComponentNotAcceptedBBClient.register_key(RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK,
                                                             access=py_trees.common.Access.WRITE)
        self.recipeComponentNotAcceptedBBClient.register_key(DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_DISPLAYED_CHECK,
                                                             access=py_trees.common.Access.WRITE)
        self.recipeComponentNotAcceptedBBClient.register_key(
            DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_DISPLAYED_CHECK,
            access=py_trees.common.Access.WRITE)

    def setup(self):
        """No delayed initialisation required for this example."""

        self.logger.debug("  %s [RecipeComponentNotAccepted::setup()]" % self.name)

    def initialise(self):
        """Reset a counter variable."""
        self.logger.debug("  %s [RecipeComponentNotAccepted::initialise()]" % self.name)

    def update(self):
        """Increment the counter and decide on a new status."""
        self.recipeComponentNotAcceptedBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                    self.recipeComponentNotAcceptedBBClient.get(
                                                        BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE))

        if self.parameter == "get_alternative":
            self.recipeComponentNotAcceptedBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S6.0")
        else:
            self.recipeComponentNotAcceptedBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S3.7")

        self.recipeComponentNotAcceptedBBClient.set(BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK, False)
        self.recipeComponentNotAcceptedBBClient.set(RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK, False)
        self.recipeComponentNotAcceptedBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_DISPLAYED_CHECK, False)
        self.recipeComponentNotAcceptedBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_DISPLAYED_CHECK, False)

        new_status = py_trees.common.Status.FAILURE
        print("BB after reset - RecipeComponentNotAccepted")
        print(self.recipeComponentNotAcceptedBBClient)

        self.feedback_message = "previous_system_state: " + str(
            self.recipeComponentNotAcceptedBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE))
        self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                       new_status, self.feedback_message))

        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""

        self.logger.debug(" %s [RecipeComponentNotAccepted::terminate().terminate()][%s->%s]" % (self.name, self.status,
                                                                                                 new_status))


class GetAlternative(py_trees.behaviour.Behaviour):
    def __init__(self, name, parameter):
        """Configure the name of the behaviour."""
        super(GetAlternative, self).__init__(name)
        self.logger.debug("%s.__init__()" % self.__class__.__name__)
        self.parameter = parameter
        print("GetAlternative - parameter: ", self.parameter)

        self.getAlternativeBBClient = self.attach_blackboard_client(
            name="getAlternativeBBClient")
        self.getAlternativeBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                 access=py_trees.common.Access.WRITE)
        self.getAlternativeBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                                 access=py_trees.common.Access.WRITE)
        self.getAlternativeBBClient.register_key(BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK,
                                                 access=py_trees.common.Access.WRITE)
        self.getAlternativeBBClient.register_key(RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK,
                                                 access=py_trees.common.Access.WRITE)
        self.getAlternativeBBClient.register_key(DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_DISPLAYED_CHECK,
                                                 access=py_trees.common.Access.WRITE)
        self.getAlternativeBBClient.register_key(
            DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_DISPLAYED_CHECK,
            access=py_trees.common.Access.WRITE)

    def setup(self):
        """No delayed initialisation required for this example."""

        self.logger.debug("  %s [getAlternativeBBClient::setup()]" % self.name)

    def initialise(self):
        """Reset a counter variable."""
        self.logger.debug("  %s [getAlternativeBBClient::initialise()]" % self.name)

    def update(self):
        """Increment the counter and decide on a new status."""
        self.getAlternativeBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE,
                                        self.getAlternativeBBClient.get(
                                            BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE))
        self.getAlternativeBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S6.0")
        new_status = py_trees.common.Status.FAILURE

        self.getAlternativeBBClient.set(BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK, False)
        self.getAlternativeBBClient.set(RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK, False)
        self.getAlternativeBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_DISPLAYED_CHECK, False)
        self.getAlternativeBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_DISPLAYED_CHECK, False)

        print("BB after reset - getAlternativeBBClient")
        print(self.getAlternativeBBClient)

        self.feedback_message = "previous_system_state: " + str(
            self.getAlternativeBBClient.get(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE))
        self.logger.debug("%s.update()[%s->%s][%s]" % (self.__class__.__name__, self.status,
                                                       new_status, self.feedback_message))

        return new_status

    def terminate(self, new_status):
        """Nothing to clean up in this example."""

        self.logger.debug(" %s [getAlternativeBBClient::terminate().terminate()][%s->%s]" % (self.name, self.status,
                                                                                             new_status))


def _update_preference(data, key, bb_in_list, bb_out_list):
    #  bb_in_list, bb_out_list => blackboard list for respective preference
    # data => data:  {'recipe_title': {'entities_in': [], 'entities_out': []},
    #                 'cuisine': {'entities_in': [], 'entities_out': [], 'input_with_entity_replacement': ''},
    #                 'menu_type': {'entities_in': [], 'entities_out': [], 'input_with_entity_replacement': ''},
    #                 'occasion': {'entities_in': [], 'entities_out': [], 'input_with_entity_replacement': ''},
    #                 'preparation': {'entities_in': [], 'entities_out': [], 'input_with_entity_replacement': ''},
    #                 'dish_type': {'entities_in': [], 'entities_out': [], 'input_with_entity_replacement': ''},
    #                 'diet_healthy': {'entities_in': [], 'entities_out': [], 'input_with_entity_replacement': ''},
    #                 'ingredients': {'entities_in': [''], 'entities_out': [], 'input_with_entity_replacement': ''}}

    # print("_update_preferences: ")
    # print("data: ", data)
    # print("key: ", key)

    if data[key]["entities_in"]:
        for entry in data[key]["entities_in"]:
            if entry in bb_out_list:
                bb_out_list.remove(entry)
            if entry not in bb_in_list:
                if key == "recipe_title":
                    bb_in_list = [entry]
                else:
                    bb_in_list.append(entry)
    if data[key]["entities_out"]:
        for entry in data[key]["entities_out"]:
            if entry in bb_in_list:
                bb_in_list.remove(entry)
            if entry not in bb_out_list:
                bb_out_list.append(entry)

    # print("Updated lists in BB: ")
    # print("IN: ", bb_in_list)
    # print("OUT: ", bb_out_list)
    return bb_in_list, bb_out_list


def update_blackboard(data):
    print("Updating BB vars in bt with this input data: ", data)
    # data is a dictionary in the form: {'ingredients_in': ['bananen'], 'current_intent': 'provide_revise_preference'}

    updateBBClient = py_trees.blackboard.Client(name="updateBlackboardWA")

    updateBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, access=py_trees.common.Access.WRITE)
    # updateBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE, access=py_trees.common.Access.WRITE)

    updateBBClient.register_key(BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK, access=py_trees.common.Access.WRITE)

    # Intents-related
    updateBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_PREVIOUS_INTENT, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_FEEDBACK, access=py_trees.common.Access.WRITE)

    # Related to User Preferences
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_ENOUGH_PREFERENCES,
                                access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_IN,
                                access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_OUT,
                                access=py_trees.common.Access.WRITE)

    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_IN, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_OUT, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_IN, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_OUT, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_IN, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_OUT,
                                access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_IN, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_OUT,
                                access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_IN, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_OUT, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_IN, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_OUT, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_IN, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_OUT, access=py_trees.common.Access.WRITE)

    # System Feedback Related to Found Recommendation
    updateBBClient.register_key(key=RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK,
                                access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECOMMENDATION_NAMESPACE + BB_KEY_REC_LIST, access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=RECOMMENDATION_NAMESPACE + BB_KEY_CURRENT_REC, access=py_trees.common.Access.WRITE)

    # Recipe Display and Acceptance
    updateBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_DISPLAYED_CHECK,
                                access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_DISPLAY_INGREDIENTS,
                                access=py_trees.common.Access.WRITE)
    updateBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_DISPLAY_INSTRUCTIONS,
                                access=py_trees.common.Access.WRITE)

    if BB_KEY_FEEDBACK in data and data[BB_KEY_FEEDBACK]:
        updateBBClient.set(INTENTS_NAMESPACE + BB_KEY_FEEDBACK, data[BB_KEY_FEEDBACK])

    # since an intent can have value 0, the last part of the check would not allow update
    if BB_KEY_CURRENT_INTENT in data:  # and data[BB_KEY_CURRENT_INTENT]:
        previous_intent = updateBBClient.get(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT)
        current_intent = data[BB_KEY_CURRENT_INTENT]
        print("==================================== UPDATING INTENT ===================================")
        print("current intent in data: ", current_intent)
        updateBBClient.set(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT, current_intent)
        updateBBClient.set(INTENTS_NAMESPACE + BB_KEY_PREVIOUS_INTENT, previous_intent)
        print("current intent in data: ", updateBBClient.get(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT))

    if "named_entities" in data and data["named_entities"]:
        for entity in data["named_entities"]:
            # print("ENTITY: ")
            # print(entity)
            bb_entity_in_list = updateBBClient.get(str(RECIPE_PARAM_NAMESPACE + entity + "_in"))
            bb_entity_out_list = updateBBClient.get(str(RECIPE_PARAM_NAMESPACE + entity + "_out"))
            bb_entity_in_list, bb_entity_out_list = _update_preference(data["named_entities"],
                                                                       entity,
                                                                       bb_entity_in_list,
                                                                       bb_entity_out_list)
            updateBBClient.set(RECIPE_PARAM_NAMESPACE + entity + "_in", bb_entity_in_list)
            updateBBClient.set(RECIPE_PARAM_NAMESPACE + entity + "_out", bb_entity_out_list)

    if BB_KEY_SEARCH_COMPLETED_CHECK in data:  # and data[BB_KEY_SEARCH_COMPLETED_CHECK]:
        # print("*********")
        # print("*********UPDATED SEARCH COMPLETED***************", data[BB_KEY_SEARCH_COMPLETED_CHECK])
        updateBBClient.set(BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK, data[BB_KEY_SEARCH_COMPLETED_CHECK])

    if BB_KEY_REC_FOUND_CHECK in data:  # and data[BB_KEY_REC_FOUND_CHECK]:
        updateBBClient.set(RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK, data[BB_KEY_REC_FOUND_CHECK])

    # check enough preferences:
    if updateBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_IN) or (
            updateBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_IN) and (
            updateBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_IN) or
            updateBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_IN) or
            updateBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_IN) or
            updateBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_IN))
    ):

        updateBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_ENOUGH_PREFERENCES, True)
        # print("JUST SET ENOUGH PREFERENCES TO TRUE")
        # print(" => ENOUGH_PREFERENCES_SET: ", updateBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_ENOUGH_PREFERENCES))
    else:
        updateBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_ENOUGH_PREFERENCES, False)
        # print("JUST SET ENOUGH PREFERENCES TO FALSE")


"""

def _reset_blackboard():
    print("\n=== RESET ===\n")
    resetBBClient = py_trees.blackboard.Client(name="resetWA")

    resetBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, access=py_trees.common.Access.WRITE)
    resetBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S2.5")

    resetBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE, access=py_trees.common.Access.WRITE)
    resetBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE, "S2.5")

    # Intents-related
    resetBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_PREVIOUS_INTENT, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_FEEDBACK, access=py_trees.common.Access.WRITE)
    resetBBClient.set(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT, "0")
    resetBBClient.set(INTENTS_NAMESPACE + BB_KEY_PREVIOUS_INTENT, "0")
    resetBBClient.set(INTENTS_NAMESPACE + BB_KEY_FEEDBACK, "neutral")

    # Related to User Preferences
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_IN, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_OUT,
                               access=py_trees.common.Access.WRITE)

    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_IN, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_OUT, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_IN, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_OUT, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_IN,
                               access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_OUT,
                               access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_IN,
                               access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_OUT,
                               access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_IN, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_OUT, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_IN, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_OUT, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_IN, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_OUT, access=py_trees.common.Access.WRITE)

    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_IN, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_OUT, [])

    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_IN, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_OUT, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_IN, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_OUT, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_IN, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_OUT, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_IN, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_OUT, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_IN, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_OUT, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_IN, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_OUT, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_IN, [])
    resetBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_OUT, [])

    # System Feedback Related to Found Recommendation
    resetBBClient.register_key(key=RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK,
                               access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECOMMENDATION_NAMESPACE + BB_KEY_REC_LIST, access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=RECOMMENDATION_NAMESPACE + BB_KEY_CURRENT_REC, access=py_trees.common.Access.WRITE)

    resetBBClient.set(RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK, False)
    resetBBClient.set(RECOMMENDATION_NAMESPACE + BB_KEY_REC_LIST, [])
    resetBBClient.set(RECOMMENDATION_NAMESPACE + BB_KEY_CURRENT_REC, {})

    # Recipe Display and Acceptance, booleans
    resetBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_ACCEPTED_CHECK,
                               access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_DISPLAY_INGREDIENTS_CHECK,
                               access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_DISPLAY_INSTRUCTIONS_CHECK,
                               access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_REC_ACCEPTED_CHECK,
                               access=py_trees.common.Access.WRITE)
    resetBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_ACCEPTED_CHECK,
                               access=py_trees.common.Access.WRITE)

    resetBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_ACCEPTED_CHECK, False)
    resetBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_DISPLAY_INGREDIENTS_CHECK, False)
    resetBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_DISPLAY_INSTRUCTIONS_CHECK, False)
    resetBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_REC_ACCEPTED_CHECK, False)
    resetBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_ACCEPTED_CHECK, False)
"""


def _reset_preferences():
    resetPreferencesBBClient = py_trees.blackboard.Client(name="resetPreferencesBBClient WA")

    # Related to User Preferences
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_ENOUGH_PREFERENCES,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_IN,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_OUT,
                                          access=py_trees.common.Access.WRITE)

    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_IN,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_OUT,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_IN,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_OUT,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_IN,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_OUT,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_IN,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_OUT,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_IN,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_OUT,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_IN,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_OUT,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_IN,
                                          access=py_trees.common.Access.WRITE)
    resetPreferencesBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_OUT,
                                          access=py_trees.common.Access.WRITE)

    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_ENOUGH_PREFERENCES, False)
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_IN, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_OUT, [])

    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_IN, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_OUT, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_IN, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_OUT, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_IN, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_OUT, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_IN, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_OUT, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_IN, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_OUT, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_IN, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_OUT, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_IN, [])
    resetPreferencesBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_OUT, [])


def _reset_search_params():
    resetSearchParamsBBClient = py_trees.blackboard.Client(name="resetSearchParamsBBClient WA")

    resetSearchParamsBBClient.register_key(key=RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK,
                                           access=py_trees.common.Access.WRITE)
    resetSearchParamsBBClient.register_key(key=BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK,
                                           access=py_trees.common.Access.WRITE)
    resetSearchParamsBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_DISPLAYED_CHECK,
                                           access=py_trees.common.Access.WRITE)
    resetSearchParamsBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_DISPLAYED_CHECK,
                                           access=py_trees.common.Access.WRITE)

    resetSearchParamsBBClient.set(RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK, False)
    resetSearchParamsBBClient.set(BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK, False)
    resetSearchParamsBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_DISPLAYED_CHECK, False)
    resetSearchParamsBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_DISPLAYED_CHECK, False)


def _reset_intent_info():
    resetIntentInfoBBClient = py_trees.blackboard.Client(name="resetIntentInfoBBClient WA")
    # Intents-related
    resetIntentInfoBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                         access=py_trees.common.Access.WRITE)
    resetIntentInfoBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_PREVIOUS_INTENT,
                                         access=py_trees.common.Access.WRITE)
    resetIntentInfoBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_FEEDBACK,
                                         access=py_trees.common.Access.WRITE)

    resetIntentInfoBBClient.set(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT, "0")
    resetIntentInfoBBClient.set(INTENTS_NAMESPACE + BB_KEY_PREVIOUS_INTENT, "0")
    resetIntentInfoBBClient.set(INTENTS_NAMESPACE + BB_KEY_FEEDBACK, "neutral")


def _reset_state_info():
    resetStateInfoBBClient = py_trees.blackboard.Client(name="resetStateInfoBBClient WA")
    resetStateInfoBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE, access=py_trees.common.Access.WRITE)
    resetStateInfoBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, access=py_trees.common.Access.WRITE)
    resetStateInfoBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE, "S2.1")
    resetStateInfoBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S2.1")


def create_root():
    # print("\n\n\n+++ STARTING CONVERSATION +++\n\n\n")
    # py_trees.logging.level = py_trees.logging.Level.DEBUG

    py_trees.blackboard.Blackboard.enable_activity_stream(maximum_size=100)
    generalBBClient = py_trees.blackboard.Client(name="GeneralWA")

    generalBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, access=py_trees.common.Access.WRITE)
    generalBBClient.set(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, "S2.1")

    generalBBClient.register_key(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE, access=py_trees.common.Access.WRITE)
    generalBBClient.set(BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE, "S2.1")

    generalBBClient.register_key(BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK, access=py_trees.common.Access.WRITE)
    generalBBClient.set(BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK, False)

    # Intents-related
    generalBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT, access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_PREVIOUS_INTENT, access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_FEEDBACK, access=py_trees.common.Access.WRITE)
    generalBBClient.set(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT, "0")
    generalBBClient.set(INTENTS_NAMESPACE + BB_KEY_PREVIOUS_INTENT, "0")
    generalBBClient.set(INTENTS_NAMESPACE + BB_KEY_FEEDBACK, "neutral")

    # Related to User Preferences
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_ENOUGH_PREFERENCES,
                                 access=py_trees.common.Access.WRITE)

    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_IN,
                                 access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_OUT,
                                 access=py_trees.common.Access.WRITE)

    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_IN, access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_OUT, access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_IN, access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_OUT, access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_IN,
                                 access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_OUT,
                                 access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_IN,
                                 access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_OUT,
                                 access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_IN, access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_OUT, access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_IN, access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_OUT, access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_IN, access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_OUT, access=py_trees.common.Access.WRITE)

    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_ENOUGH_PREFERENCES, False)

    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_IN, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_OUT, [])

    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_IN, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_OUT, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_IN, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_OUT, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_IN, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_OUT, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_IN, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_OUT, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_IN, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_OUT, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_IN, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_OUT, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_IN, [])
    generalBBClient.set(RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_OUT, [])

    # System Feedback Related to Found Recommendation
    generalBBClient.register_key(key=RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK,
                                 access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECOMMENDATION_NAMESPACE + BB_KEY_REC_LIST, access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=RECOMMENDATION_NAMESPACE + BB_KEY_CURRENT_REC, access=py_trees.common.Access.WRITE)

    generalBBClient.set(RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK, False)
    generalBBClient.set(RECOMMENDATION_NAMESPACE + BB_KEY_REC_LIST, [])
    generalBBClient.set(RECOMMENDATION_NAMESPACE + BB_KEY_CURRENT_REC, {})

    # Recipe Display and Acceptance, booleans
    generalBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_DISPLAYED_CHECK,
                                 access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_DISPLAY_INGREDIENTS,
                                 access=py_trees.common.Access.WRITE)
    generalBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_DISPLAYED_CHECK,
                                 access=py_trees.common.Access.WRITE)

    generalBBClient.register_key(key=DISPLAY_PARAM_NAMESPACE + BB_KEY_DISPLAY_INSTRUCTIONS,
                                 access=py_trees.common.Access.WRITE)

    generalBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_TITLE_DISPLAYED_CHECK, False)
    generalBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_DISPLAY_INGREDIENTS, False)
    generalBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_DISPLAYED_CHECK, False)
    generalBBClient.set(DISPLAY_PARAM_NAMESPACE + BB_KEY_DISPLAY_INSTRUCTIONS, False)
    #######################################################################################
    ###ELICIT PREFERRENCES: INGREDIENT_IN or any of the MENU, CUISINE, OCCASION
    #######################################################################################
    # elicit ingredient_in as first condition

    isIngredientInSet = py_trees.behaviours.CheckBlackboardVariableValue(
        name=BB_KEY_INGREDIENTS_IN,
        check=py_trees.common.ComparisonExpression(
            variable=RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_IN,
            value=[],
            operator=operator.eq
        )
    )

    setIngredientsValue = EnterIngredientValue(name="EnterIngredientValues")
    setIngredientsValueDecorator = py_trees.decorators.RunningIsFailure(child=setIngredientsValue)

    #########################################################################
    isFurtherPreferenceSet = py_trees.behaviours.CheckBlackboardVariableValues(
        name="furtherPreferenceCheck",
        checks=[py_trees.common.ComparisonExpression(variable=RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_IN,
                                                     operator=operator.ne, value=[]),
                py_trees.common.ComparisonExpression(variable=RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_IN,
                                                     operator=operator.ne, value=[]),
                py_trees.common.ComparisonExpression(variable=RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_IN,
                                                     operator=operator.ne, value=[]),
                py_trees.common.ComparisonExpression(variable=RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_IN,
                                                     operator=operator.ne, value=[])
                ],
        operator=operator.or_
    )

    setFurtherPreference = EnterFurtherPreference(name="EnterFurtherPreference")
    setFurtherPreferenceDecorator = py_trees.decorators.RunningIsFailure(child=setFurtherPreference)

    furtherPreferenceSelector = py_trees.composites.Selector(name="checkSetFurtherPreferenceSel")
    furtherPreferenceSelector.add_children([isFurtherPreferenceSet, setFurtherPreferenceDecorator])

    ingredientsOrFurtherPreferenceSelector = py_trees.composites.Selector(name="ingredientsOrFurtherPreferenceSel")
    ingredientsOrFurtherPreferenceSelector.add_children([isIngredientInSet, furtherPreferenceSelector])

    elicitPreferencesSubtree = py_trees.composites.Sequence(name="ElicitPreferencesSubtree")
    elicitPreferencesSubtree.add_children([ingredientsOrFurtherPreferenceSelector, setIngredientsValueDecorator])

    elicitPreferencesSubtreeDecorator = py_trees.decorators.SuccessIsFailure(child=elicitPreferencesSubtree)

    #######################################################################################
    ### DISPLAY TITLE AND FEEDBACK
    #######################################################################################

    checkDisplayedTitle = py_trees.behaviours.CheckBlackboardVariableValue(
        name="titleDisplayed?",
        check=py_trees.common.ComparisonExpression(variable=BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, value="S3.1",
                                                   operator=operator.eq)
    )
    displayRecipeTitle = DisplayRecommendationComponent(name="DisplayRecipeTitle",
                                                        display_component=BB_KEY_DISPLAY_TITLE)
    displayTitleSelector = py_trees.composites.Selector(name="DisplayRecipeTitle?")
    displayTitleSelector.add_children([checkDisplayedTitle, displayRecipeTitle])

    ###############################################################################################
    checkTitleIntentGetAlternative = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentGetAlternative?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.GET_ALTERNATIVES, operator=operator.eq)
    )
    getAlternativeWhenTitle = RecipeComponentNotAccepted(name="GetAlternative",
                                                         parameter="get_alternative")
    getAlternativeWhenTitleSeq = py_trees.composites.Sequence(name="getAlternativeWhenTitleSeq")
    getAlternativeWhenTitleSeq.add_children([checkTitleIntentGetAlternative, getAlternativeWhenTitle])

    ###############################################################################################

    checkIntentProvideRevisePreferencesWhenTitle = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentProvideRevisePreferences?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.PROVIDE_REVISE_PREFERENCES, operator=operator.eq)
    )
    provideRevisePreferencesWhenTitle = RecipeComponentNotAccepted(name="ProvideRevisePreferences",
                                                                   parameter=BB_KEY_DISPLAY_TITLE)
    preferencesOrAlternativeWhenTitleSeq = py_trees.composites.Sequence(name="preferencesOrAlternativeWhenTitleSeq")
    preferencesOrAlternativeWhenTitleSeq.add_children(
        [checkIntentProvideRevisePreferencesWhenTitle, provideRevisePreferencesWhenTitle])

    ################################################################################################
    checkTitleFBPositiveOrNeutral = py_trees.behaviours.CheckBlackboardVariableValues(
        name="isFBPositiveOrNeutral?",
        checks=[py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_FEEDBACK, value="positive",
                                                     operator=operator.eq),
                py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_FEEDBACK, value="neutral",
                                                     operator=operator.eq)
                ],
        operator=operator.or_
    )
    recipeTitleNotAccepted = RecipeComponentNotAccepted(name="TitleNotAccepted",
                                                        parameter=BB_KEY_DISPLAY_TITLE)
    FBCheckAndTitleNotAcceptedSel = py_trees.composites.Selector("FBCheckAndTitleNotAcceptedSel")
    FBCheckAndTitleNotAcceptedSel.add_children([checkTitleFBPositiveOrNeutral, recipeTitleNotAccepted])

    ##############################################################################
    checkTitleFeedbackIntent = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentFeedback?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.USER_FEEDBACK, operator=operator.eq)
    )
    isFBIntentFollowingTitleDisplaySeq = py_trees.composites.Sequence(name="IsFBIntentFollowingTitleDisplaySeq")
    isFBIntentFollowingTitleDisplaySeq.add_children([checkTitleFeedbackIntent, FBCheckAndTitleNotAcceptedSel])

    ####################################################################################################################

    checkSkipTitleDisplay = py_trees.behaviours.CheckBlackboardVariableValues(
        name="skipTitle?",
        checks=[py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                     value=C.DISPLAY_INSTRUCTIONS, operator=operator.eq),
                py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                     value=C.DISPLAY_INGREDIENTS, operator=operator.eq)],
        operator=operator.or_
    )

    skipPreferencesAlternativeOrFBTitleSel = py_trees.composites.Selector(name="skipPreferencesAlternativeOrFBTitleSel")
    skipPreferencesAlternativeOrFBTitleSel.add_children([checkSkipTitleDisplay,
                                                         preferencesOrAlternativeWhenTitleSeq,
                                                         getAlternativeWhenTitleSeq,
                                                         isFBIntentFollowingTitleDisplaySeq
                                                         ])
    ####################################################################################################################

    displayTitleSubtree = py_trees.composites.Sequence(name="DisplayTitleSubtree")
    displayTitleSubtree.add_children([displayTitleSelector, skipPreferencesAlternativeOrFBTitleSel])

    checkPreviousStateWhenTitle = py_trees.behaviours.CheckBlackboardVariableValues(
        name="previousStateIsDisplayIngredients?",
        checks=[py_trees.common.ComparisonExpression(variable=BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE, value="S3.3",
                                                     operator=operator.eq),
                py_trees.common.ComparisonExpression(variable=BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE, value="S3.5",
                                                     operator=operator.eq)],
        operator=operator.or_
    )
    displayTitleOrIngredientsSelector = py_trees.composites.Selector(name="displayTitleOrIngredientsSel")
    displayTitleOrIngredientsSelector.add_children([checkPreviousStateWhenTitle, displayTitleSubtree])

    #######################################################################################
    ### DISPLAY INGREDIENTS
    #######################################################################################s
    """
    checkDisplayedIngredients = py_trees.behaviours.CheckBlackboardVariableValues(
        name="ingredientsDisplayed?",
        checks=[py_trees.common.ComparisonExpression(variable=BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, value="S3.3",
                                                     operator=operator.eq),
                py_trees.common.ComparisonExpression(
                    variable=DISPLAY_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_DISPLAYED_CHECK,
                    value=True, operator=operator.eq)],
        operator=operator.or_
    )
    """
    checkDisplayedIngredients = py_trees.behaviours.CheckBlackboardVariableValue(
        name="ingredientsDisplayed?",
        check=py_trees.common.ComparisonExpression(variable=BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, value="S3.3",
                                                   operator=operator.eq)
    )

    displayIngredients = DisplayRecommendationComponent(name="DisplayIngredients",
                                                        display_component=BB_KEY_DISPLAY_INGREDIENTS)
    displayIngredientsSelector = py_trees.composites.Selector(name="DisplayIngredients?")
    displayIngredientsSelector.add_children([checkDisplayedIngredients, displayIngredients])

    checkSkipIngredientsDisplay = py_trees.behaviours.CheckBlackboardVariableValue(
        name="jumpToInstructions?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.DISPLAY_INSTRUCTIONS, operator=operator.eq)
    )

    checkIngredientsIntentGetAlternative = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentGetAlternative?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.GET_ALTERNATIVES, operator=operator.eq)
    )

    getAlternativeForIngredients = RecipeComponentNotAccepted(name="GetAlternative",
                                                              parameter="get_alternative")
    getAlternativeForIngredientsSequence = py_trees.composites.Sequence(name="GetAlternativeForIngredients")
    getAlternativeForIngredientsSequence.add_children([checkIngredientsIntentGetAlternative,
                                                       getAlternativeForIngredients])

    checkIntentProvideRevisePreferencesWhenIngredients = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentProvideRevisePreferences?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.PROVIDE_REVISE_PREFERENCES, operator=operator.eq)
    )
    provideRevisePreferencesWhenIngredients = RecipeComponentNotAccepted(name="ProvideRevisePreferences",
                                                                         parameter=BB_KEY_DISPLAY_INGREDIENTS)
    provideRevisePreferencesWhenIngredientsSeq = py_trees.composites.Sequence(
        name="provideRevisePreferencesWhenIngredientsSeq")
    provideRevisePreferencesWhenIngredientsSeq.add_children([checkIntentProvideRevisePreferencesWhenIngredients,
                                                             provideRevisePreferencesWhenIngredients])

    checkIngredientsFeedbackIntent = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentFeedback?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.USER_FEEDBACK, operator=operator.eq)
    )

    checkIngredientsFBPositiveOrNeutral = py_trees.behaviours.CheckBlackboardVariableValues(
        name="isFBPositiveOrNeutral?",
        checks=[py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_FEEDBACK, value="positive",
                                                     operator=operator.eq),
                py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_FEEDBACK, value="neutral",
                                                     operator=operator.eq)
                ],
        operator=operator.or_
    )

    recipeIngredientsNotAccepted = RecipeComponentNotAccepted(name="IngredientsNotAccepted",
                                                              parameter=BB_KEY_DISPLAY_INGREDIENTS)

    fbCheckAndIngredientsNotAcceptedSelector = py_trees.composites.Selector("FBCheckAndIngredientsNotAccepted")
    fbCheckAndIngredientsNotAcceptedSelector.add_children([checkIngredientsFBPositiveOrNeutral,
                                                           recipeIngredientsNotAccepted])

    isFBIntentFollowingIngredientsDisplaySequence = py_trees.composites.Sequence(
        name="IsFBIntentFollowingIngredientsDisplay")
    isFBIntentFollowingIngredientsDisplaySequence.add_children([checkIngredientsFeedbackIntent,
                                                                fbCheckAndIngredientsNotAcceptedSelector])

    skipAlternativeOrFBIngredientsSelector = py_trees.composites.Selector(name="SkipAlternativeOrFBIngredients")
    skipAlternativeOrFBIngredientsSelector.add_children([checkSkipIngredientsDisplay,
                                                         provideRevisePreferencesWhenIngredientsSeq,
                                                         getAlternativeForIngredientsSequence,
                                                         isFBIntentFollowingIngredientsDisplaySequence])

    displayIngredientsSubtree = py_trees.composites.Sequence(name="DisplayIngredientsSubtree")
    displayIngredientsSubtree.add_children([displayIngredientsSelector, skipAlternativeOrFBIngredientsSelector])

    checkPreviousStateWhenIngredients = py_trees.behaviours.CheckBlackboardVariableValue(
        name="previousStateIsDisplayInstructions?",
        check=py_trees.common.ComparisonExpression(variable=BB_SLASH + BB_KEY_PREVIOUS_SYSTEM_STATE, value="S3.5",
                                                   operator=operator.eq)
    )
    displayIngredientsOrInstructionsSelector = py_trees.composites.Selector(name="displayTitleOrIngredientsSel")
    displayIngredientsOrInstructionsSelector.add_children(
        [checkPreviousStateWhenIngredients, displayIngredientsSubtree])

    #######################################################################################
    ### DISPLAY INSTRUCTIONS
    #######################################################################################
    checkDisplayedInstructions = py_trees.behaviours.CheckBlackboardVariableValue(
        name="instructionsDisplayed?",
        check=py_trees.common.ComparisonExpression(variable=BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, value="S3.5",
                                                   operator=operator.eq)
    )
    """
    checkDisplayedInstructions = py_trees.behaviours.CheckBlackboardVariableValues(
        name="instructionsDisplayed?",
        checks=[py_trees.common.ComparisonExpression(variable=BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, value="S3.5",
                                                     operator=operator.eq),
                py_trees.common.ComparisonExpression(
                    variable=DISPLAY_PARAM_NAMESPACE + BB_KEY_INSTRUCTIONS_DISPLAYED_CHECK,
                    value=True, operator=operator.eq)],
        operator=operator.or_
    )
    """
    displayInstructions = DisplayRecommendationComponent(name="DisplayInstructions",
                                                         display_component=BB_KEY_DISPLAY_INSTRUCTIONS)

    displayInstructionsSelector = py_trees.composites.Selector(name="DisplayInstructions?")
    displayInstructionsSelector.add_children([checkDisplayedInstructions, displayInstructions])

    checkInstructionsIntentGetAlternative = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentGetAlternative?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.GET_ALTERNATIVES, operator=operator.eq)
    )

    getAlternativeForInstructions = RecipeComponentNotAccepted(name="GetAlternative",
                                                               parameter="get_alternative")
    getAlternativeForInstructionsSequence = py_trees.composites.Sequence(name="GetAlternativeForInstructions")
    getAlternativeForInstructionsSequence.add_children([checkInstructionsIntentGetAlternative,
                                                        getAlternativeForInstructions])

    checkIntentProvideRevisePreferencesWhenInstructions = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentProvideRevisePreferences?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.PROVIDE_REVISE_PREFERENCES, operator=operator.eq)
    )
    provideRevisePreferencesWhenInstructions = RecipeComponentNotAccepted(name="ProvideRevisePreferences",
                                                                          parameter=BB_KEY_DISPLAY_INGREDIENTS)
    provideRevisePreferencesWhenInstructionsSeq = py_trees.composites.Sequence(
        name="provideRevisePreferencesWhenIngredientsSeq")
    provideRevisePreferencesWhenInstructionsSeq.add_children([checkIntentProvideRevisePreferencesWhenInstructions,
                                                              provideRevisePreferencesWhenInstructions])

    checkInstructionsFeedbackIntent = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentFeedback?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.USER_FEEDBACK, operator=operator.eq)
    )

    checkInstructionsFBPositiveOrNeutral = py_trees.behaviours.CheckBlackboardVariableValues(
        name="isFBPositiveOrNeutral?",
        checks=[py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_FEEDBACK, value="positive",
                                                     operator=operator.eq),
                py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_FEEDBACK, value="neutral",
                                                     operator=operator.eq)
                ],
        operator=operator.or_
    )

    recipeInstructionsNotAccepted = RecipeComponentNotAccepted(name="InstructionsNotAccepted",
                                                               parameter=BB_KEY_DISPLAY_INSTRUCTIONS)

    fbCheckAndInstructionsNotAcceptedSelector = py_trees.composites.Selector("FBCheckAndInstructionsNotAccepted")
    fbCheckAndInstructionsNotAcceptedSelector.add_children([checkInstructionsFBPositiveOrNeutral,
                                                            recipeInstructionsNotAccepted])

    isFBIntentFollowingInstructionsDisplaySequence = py_trees.composites.Sequence(
        name="isFBIntentFollowingInstructionsDisplay")
    isFBIntentFollowingInstructionsDisplaySequence.add_children([checkInstructionsFeedbackIntent,
                                                                 fbCheckAndInstructionsNotAcceptedSelector])

    skipAlternativeOrFBInstructionsSelector = py_trees.composites.Selector(name="SkipAlternativeOrFBInstructions")
    skipAlternativeOrFBInstructionsSelector.add_children([  # checkSkipInstructionsDisplay,
        provideRevisePreferencesWhenInstructionsSeq,
        getAlternativeForInstructionsSequence,
        isFBIntentFollowingInstructionsDisplaySequence])

    displayInstructionsSubtree = py_trees.composites.Sequence(name="DisplayInstructionsSubtree")
    displayInstructionsSubtree.add_children([displayInstructionsSelector, skipAlternativeOrFBInstructionsSelector])

    ######################################################################################
    ### RESET PREFERECES SUBTREE
    #######################################################################################
    checkAskedForConfirmationResetConversation = py_trees.behaviours.CheckBlackboardVariableValue(
        name="askedForConfirmation?",
        check=py_trees.common.ComparisonExpression(variable=BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, value="S5.1",
                                                   operator=operator.eq)
    )
    confirmResetPreferences = ConfirmResetPreferences("ConfirmReset")

    resetConfirmSelector = py_trees.composites.Selector(name="ResetConfirmSelector")
    resetConfirmSelector.add_children([checkAskedForConfirmationResetConversation, confirmResetPreferences])

    checkResetFeedbackIntent = py_trees.behaviours.CheckBlackboardVariableValues(
        name="isIntentFBAndPositive?",
        checks=[py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                     value=C.USER_FEEDBACK, operator=operator.eq),
                py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_FEEDBACK, value="positive",
                                                     operator=operator.eq)
                ],
        operator=operator.and_
    )

    resetConversation = ResetPreferences("Reset")
    resetConfirmedSequence = py_trees.composites.Sequence(name="ResetConfirmed")
    resetConfirmedSequence.add_children([checkResetFeedbackIntent, resetConversation])

    checkPrefsOrAltIntentWhenReset = py_trees.behaviours.CheckBlackboardVariableValues(
        name="isIntentRevisePrefsOrAlt?",
        checks=[py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                     value=C.PROVIDE_REVISE_PREFERENCES, operator=operator.eq),
                py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                     value=C.GET_ALTERNATIVES, operator=operator.eq)
                ],
        operator=operator.or_
    )

    resetSearchParams = ResetPreferences("Reset")
    prefsOrAltWhenResetSequence = py_trees.composites.Sequence(name="RevisePrefsOrAlternative")
    prefsOrAltWhenResetSequence.add_children([checkPrefsOrAltIntentWhenReset, resetSearchParams])

    resetNotConfirmedActions = ResetNotConfirmed("ResetNotConfirmed")

    resetConfirmedSelector = py_trees.composites.Selector(name="ResetConfirmed?")
    resetConfirmedSelector.add_children([resetConfirmedSequence,
                                         prefsOrAltWhenResetSequence,
                                         resetNotConfirmedActions])

    resetConfirmedDecorator = py_trees.decorators.SuccessIsFailure(child=resetConfirmedSelector)

    resetIntentSubtree = py_trees.composites.Sequence(name="ResetIntentSubtree")
    resetIntentSubtree.add_children([resetConfirmSelector, resetConfirmedDecorator])

    ######################################################################################
    ### END CONVERSATION SUBTREE
    #######################################################################################
    checkAskedForConfirmationEndConversation = py_trees.behaviours.CheckBlackboardVariableValue(
        name="askedForConfirmation?",
        check=py_trees.common.ComparisonExpression(variable=BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, value="S4.1",
                                                   operator=operator.eq)
    )
    confirmEndConversation = ConfirmEndConversation("ConfirmEnd")

    confirmEndSelector = py_trees.composites.Selector(name="ConfirmEndSelector")
    confirmEndSelector.add_children([checkAskedForConfirmationEndConversation, confirmEndConversation])

    checkEndFeedbackIntent = py_trees.behaviours.CheckBlackboardVariableValues(
        name="isIntentFBAndPositive?",
        checks=[py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                     value=C.USER_FEEDBACK, operator=operator.eq),
                py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_FEEDBACK, value="positive",
                                                     operator=operator.eq)
                ],
        operator=operator.and_
    )

    checkPrefsOrAltIntentWhenEnd = py_trees.behaviours.CheckBlackboardVariableValues(
        name="isIntentRevisePrefsOrAlt?",
        checks=[py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                     value=C.PROVIDE_REVISE_PREFERENCES, operator=operator.eq),
                py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                     value=C.GET_ALTERNATIVES, operator=operator.eq)
                ],
        operator=operator.or_
    )

    endConversation = EndConversation("End")
    resetPrefsWhenPrefOrAlternative = ResetPreferences("Reset")
    endConfirmedSequence = py_trees.composites.Sequence(name="EndConfirmed?")
    endConfirmedSequence.add_children([checkEndFeedbackIntent, endConversation])

    prefsOrAltWhenEndSequence = py_trees.composites.Sequence(name="RevisePrefsOrAlternative")
    prefsOrAltWhenEndSequence.add_children([checkPrefsOrAltIntentWhenEnd, resetPrefsWhenPrefOrAlternative])

    endNotConfirmedActions = EndNotConfirmed("EndNotConfirmed")

    endConfirmedSelector = py_trees.composites.Selector(name="EndConfirmed?")
    endConfirmedSelector.add_children([endConfirmedSequence,
                                       prefsOrAltWhenEndSequence,
                                       endNotConfirmedActions])

    endIntentSubtree = py_trees.composites.Sequence(name="endIntentSubtree")
    endIntentSubtree.add_children([confirmEndSelector, endConfirmedSelector])
    #######################################################################################

    checkEndConversationIntent = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentEndConversation?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.QUIT, operator=operator.eq)
    )

    checkResetConversationIntent = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentResetPreferences?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.RESET_PREFERENCES, operator=operator.eq)
    )

    checkEnoughPreferencesSet = py_trees.behaviours.CheckBlackboardVariableValue(
        name="needMorePreferences?",
        check=py_trees.common.ComparisonExpression(variable=RECIPE_PARAM_NAMESPACE + BB_KEY_ENOUGH_PREFERENCES,
                                                   value=False, operator=operator.eq)
    )

    naturalConversationEnd = EndConversation(name="End")
    naturalEndDecorator = py_trees.decorators.SuccessIsFailure(child=naturalConversationEnd)

    #######################################################################################
    ###SEARCH FOR RECOMMENDATION
    #######################################################################################

    checkSearchPerformed = py_trees.behaviours.CheckBlackboardVariableValue(
        name="searchCompleted?",
        check=py_trees.common.ComparisonExpression(
            variable=BB_SLASH + BB_KEY_SEARCH_COMPLETED_CHECK,
            value=True,
            operator=operator.eq)
    )
    checkRecommendationFoundBBState = py_trees.behaviours.CheckBlackboardVariableValue(
        name="recommendationFound?",
        check=py_trees.common.ComparisonExpression(
            variable=RECOMMENDATION_NAMESPACE + BB_KEY_REC_FOUND_CHECK,
            value=True,
            operator=operator.eq)
    )
    searchRecipe = FindRecipeRecommendation(name="Search")
    noRecipeFound = NoRecipeFound(name="NoRecipeFound")
    noRecipeFoundDecorator = py_trees.decorators.SuccessIsFailure(child=noRecipeFound)

    notFoundSelector = py_trees.composites.Selector(name="notFoundOrRecommendSel")
    notFoundSelector.add_children([checkRecommendationFoundBBState, noRecipeFoundDecorator])

    #######################################################################################
    ###
    ######################################################################################
    anyCheckImageDisplay = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentDisplayImage?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.DISPLAY_IMAGES, operator=operator.eq)
    )
    checkImageDisplayed = py_trees.behaviours.CheckBlackboardVariableValue(
        name="imageDisplayed?",
        check=py_trees.common.ComparisonExpression(variable=BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                   value="S3.9", operator=operator.eq)
    )
    anyImageDisplay = DisplayRecommendationComponent(name="anyImageDisplay",
                                                     display_component="display_images")
    anyImageDisplaySelector = py_trees.composites.Selector(name="anyImageDisplaySel")
    anyImageDisplaySelector.add_children([checkImageDisplayed, anyImageDisplay])
    # anyImageDisplaySelectorDecorator = py_trees.decorators.RunningIsFailure(child=anyImageDisplaySelector)

    anyImageDisplaySeq = py_trees.composites.Sequence(name="anyImageDisplaySeq")
    anyImageDisplaySeq.add_children([anyCheckImageDisplay, anyImageDisplaySelector])
    #########################################################################
    anyCheckExtrasDisplay = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentDisplayExtras?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.DISPLAY_DETAILS, operator=operator.eq)
    )

    checkExtrasDisplayed = py_trees.behaviours.CheckBlackboardVariableValue(
        name="extrasDisplayed?",
        check=py_trees.common.ComparisonExpression(variable=BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE,
                                                   value="S3.8", operator=operator.eq)
    )

    anyExtrasDisplay = DisplayRecommendationComponent(name="anyDisplay",
                                                      display_component="display_details")
    anyExtrasDisplaySelector = py_trees.composites.Selector(name="anyExtrasDisplaySel")
    anyExtrasDisplaySelector.add_children([checkExtrasDisplayed, anyExtrasDisplay])

    anyExtrasDisplaySeq = py_trees.composites.Sequence(name="anyExtrasDisplaySeq")
    anyExtrasDisplaySeq.add_children([anyCheckExtrasDisplay, anyExtrasDisplaySelector])

    #########################################################################
    """
    anyCheckIngredientsDisplay = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentDisplayIngredients?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.DISPLAY_INGREDIENTS, operator=operator.eq)
    )
    anyIngredientsDisplay = DisplayRecommendationComponent(name="anyDisplay",
                                                           display_component="BB_KEY_DISPLAY_INGREDIENTS_CHECK")
    anyIngredientsDisplaySeq = py_trees.composites.Sequence(name="anyIngredientsDisplaySeq")
    anyIngredientsDisplaySeq.add_children([anyCheckIngredientsDisplay, anyIngredientsDisplay])

    anyCheckInstructionsDisplay = py_trees.behaviours.CheckBlackboardVariableValue(
        name="isIntentDisplayInstructions?",
        check=py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                   value=C.DISPLAY_INSTRUCTIONS, operator=operator.eq)
    )
    anyInstructionsDisplay = DisplayRecommendationComponent(name="anyDisplay",
                                                            display_component=BB_KEY_DISPLAY_INSTRUCTIONS)
    anyInstructionsDisplaySeq = py_trees.composites.Sequence(name="anyInstructionsDisplaySeq")
    anyInstructionsDisplaySeq.add_children([anyCheckInstructionsDisplay, anyInstructionsDisplay])
    
    """
    ###############################################################################

    whichComponentSelector = py_trees.composites.Selector(name="whichComponentSel")
    whichComponentSelector.add_children([anyImageDisplaySeq,
                                         anyExtrasDisplaySeq
                                         # anyIngredientsDisplaySeq,
                                         # anyInstructionsDisplaySeq
                                         ])
    whichComponentSelectorDecorator = py_trees.decorators.SuccessIsFailure(child=whichComponentSelector)

    checkIntentDisplayAnyComponent = py_trees.behaviours.CheckBlackboardVariableValues(
        name="displayAnyComponent?",
        checks=[py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                     value=C.DISPLAY_DETAILS, operator=operator.eq),
                py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                                     value=C.DISPLAY_IMAGES, operator=operator.eq)],
        # py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
        #                                     value=C.DISPLAY_INGREDIENTS, operator=operator.eq),
        # py_trees.common.ComparisonExpression(variable=INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
        #                                     value=C.DISPLAY_INSTRUCTIONS, operator=operator.eq)],
        operator=operator.or_
    )

    displayComponentsSequence = py_trees.composites.Sequence(name="displayComponentsSel")
    displayComponentsSequence.add_children([checkIntentDisplayAnyComponent, whichComponentSelectorDecorator])

    ####################################################
    recommendSequence = py_trees.composites.Sequence(name="recommendSeq")
    recommendSequence.add_children([displayTitleOrIngredientsSelector,
                                    displayIngredientsOrInstructionsSelector,
                                    displayInstructionsSubtree,
                                    naturalEndDecorator])

    recommendSelector = py_trees.composites.Selector(name="recommendSel")
    recommendSelector.add_children([displayComponentsSequence, recommendSequence])

    ####################################################
    notFoundOrRecommendSequence = py_trees.composites.Sequence(name="notFoundOrRecommendSeq")
    notFoundOrRecommendSequence.add_children([notFoundSelector, recommendSelector])

    searchSelector = py_trees.composites.Selector(name="SearchOrRecommendSel")
    searchSelector.add_children([checkSearchPerformed, searchRecipe])

    ####################################################
    searchOrRecommendSequence = py_trees.composites.Sequence(name="SearchOrRecommendSeq")
    searchOrRecommendSequence.add_children([searchSelector, notFoundOrRecommendSequence])

    elicitOrRecommendSelector = py_trees.composites.Selector(name="ElicitOrRecommendSel")
    elicitOrRecommendSelector.add_children([checkEnoughPreferencesSet, searchOrRecommendSequence])

    ####################################################
    elicitOrRecommendSequence = py_trees.composites.Sequence(name="ElicitOrRecommendSeq")
    elicitOrRecommendSequence.add_children([elicitOrRecommendSelector, elicitPreferencesSubtreeDecorator])

    resetOrRecommendSelector = py_trees.composites.Selector(name="ResetOrRecommendSel")
    resetOrRecommendSelector.add_children([checkResetConversationIntent, elicitOrRecommendSequence])

    ####################################################
    resetOrRecommendSequence = py_trees.composites.Sequence(name="ResetOrRecommendSel")
    resetOrRecommendSequence.add_children([resetOrRecommendSelector, resetIntentSubtree])

    endOrRecommendSelector = py_trees.composites.Selector(name="EndOrRecommend")
    endOrRecommendSelector.add_children([checkEndConversationIntent, resetOrRecommendSequence])

    ####################################################
    root = py_trees.composites.Sequence(name="CRS_Food")
    root.add_children([endOrRecommendSelector, endIntentSubtree])

    return root


def tree_stewardship(root):
    py_trees.logging.level = py_trees.logging.Level.DEBUG
    py_trees.display.render_dot_tree(root)

    # print("<----------------- tree_stewardship --------------->")
    ####################
    # Tree Stewardship
    ####################
    behaviour_tree = py_trees.trees.BehaviourTree(root)
    behaviour_tree.visitors.append(py_trees.visitors.DebugVisitor())
    snapshot_visitor = py_trees.visitors.SnapshotVisitor()
    behaviour_tree.visitors.append(snapshot_visitor)
    behaviour_tree.setup(timeout=5)

    # sys.exit()


def get_state():
    stateGetterBBClient = py_trees.blackboard.Client(name="stateGetterBBClientRA")

    stateGetterBBClient.register_key(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE, access=py_trees.common.Access.READ)
    current_state = stateGetterBBClient.get(BB_SLASH + BB_KEY_CURRENT_SYSTEM_STATE)

    return current_state


def get_blackboard_preferences():
    preferencesGetterBBClient = py_trees.blackboard.Client(name="preferencesGetterBBClient RA")

    # Related to User Preferences
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_IN,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_OUT,
                                           access=py_trees.common.Access.READ)

    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_IN,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_OUT,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_IN,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_OUT,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_IN,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_OUT,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_IN,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_OUT,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_IN,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_OUT,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_IN,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_OUT,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_IN,
                                           access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(key=RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_OUT,
                                           access=py_trees.common.Access.READ)

    preferencesGetterBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_FEEDBACK, access=py_trees.common.Access.READ)
    preferencesGetterBBClient.register_key(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT,
                                           access=py_trees.common.Access.READ)

    extracted_entities = {
        "named_entities": {
            "recipe_title": {
                "entities_in": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_IN),
                "entities_out": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_RECIPE_TITLE_OUT)},
            "cuisine": {"entities_in": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_IN),
                        "entities_out": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_CUISINE_OUT)},
            "menu_type": {"entities_in": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_IN),
                          "entities_out": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_MENU_TYPE_OUT)},
            "occasion": {"entities_in": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_IN),
                         "entities_out": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_OCCASION_OUT)},
            "preparation": {
                "entities_in": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_IN),
                "entities_out": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_PREPARATION_OUT)},
            "dish_type": {"entities_in": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_IN),
                          "entities_out": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_DISH_TYPE_OUT)},
            "diet_healthy": {"entities_in": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_IN),
                             "entities_out": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_DIET_OUT)},
            "ingredients": {
                "entities_in": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_IN),
                "entities_out": preferencesGetterBBClient.get(RECIPE_PARAM_NAMESPACE + BB_KEY_INGREDIENTS_OUT)}
        },
        "current_intent": preferencesGetterBBClient.get(INTENTS_NAMESPACE + BB_KEY_CURRENT_INTENT),
        "feedback": preferencesGetterBBClient.get(INTENTS_NAMESPACE + BB_KEY_FEEDBACK)
    }

    return extracted_entities
