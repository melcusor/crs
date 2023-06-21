import pathlib
import re

from recipesDBConnect import sql_alchemy_connect as sql_alchemy
from sentence_transformers import util
from NLU import CONSTANTS as C
import pickle





def _read_embeddings_for_recipe_similarity():
    # Load sentences & embeddings from disc
    path = pathlib.Path().parent.resolve() / C.EMBEDDINGS_PICKLE_FILE_PATH / C.EMBEDDINGS_PICKLE_FILE_NAME
    with open(path, "rb") as fIn:
        stored_data = pickle.load(fIn)
        # stored_sentences = stored_data['sentences']
        # stored_embeddings = stored_data['embeddings'] # embedding shape: (308714, 512)
    return stored_data


class RecipeRecommender:
    """
    The recommender:
    - receives preferences from the manager and passes them to the sql_alchemy module to retrieve a
    recommendation from the kochbar_recipes db
    - it keeps track of already made recommendations through the made_recommendations_list to prevent recommending
    recipes that have been already viewed => consider this when retrieving new recommendations from the db as well as
    when searching for similar recipes
    - it is able to compute similarities between all recipes in the db using the embeddings stored in the pickle file

    """

    def __init__(self):
        self.db = sql_alchemy.KochbarDB()
        self.embeddings = _read_embeddings_for_recipe_similarity()

        self.current_recommendation_index = None
        self.made_recommendations_list = []

    def get_recommendation(self, preferences):
        """
        :param preferences: is an object containing user preferences:

        named_entities = {"recipe_title": {"entities_in": [],
                                           "entities_out": []
                                          },
                          "cuisine": {"entities_in": [],
                                      "entities_out": []
                                     },
                          "menu_type": {"entities_in": [],
                                        "entities_out": []
                                       },
                          "occasion": {"entities_in": [],
                                       "entities_out": []
                                      },
                          "preparation": {"entities_in": [],
                                          "entities_out": []
                                         },
                          "dish_type": {"entities_in": [],
                                        "entities_out": []
                                       },
                          "diet_healthy": {"entities_in": [],
                                           "entities_out": []
                                          },
                          "ingredients": {"entities_in": [],
                                          "entities_out": []
                                         }
                }

        :return:
        - None, if no recipe according to preferences found, or
        - title of recipe if recipe found in db
        """

        # [] needed for the case where we have a list of indices of similar recipes => get_similar_recommendation below
        self.current_recommendation_index = self.db.get_recommendation(preferences, self.made_recommendations_list, [])

        if self.current_recommendation_index is not None:
            # print("RECOMMENDER - get-recommendation: ", self.current_recommendation_index)
            self.made_recommendations_list.append(self.current_recommendation_index)
        return self.current_recommendation_index

    def get_title(self, recipe_index):
        title = self.db.get_title_for_index(recipe_index)
        title = re.sub(r'\%x\d+', ' ', title)
        title = re.sub('\W+', ' ', title)
        return title

    def get_ingredients(self, recipe_index):
        ingredients = self.db.get_ingredients_for_index(recipe_index)
        ingredients = re.sub(r'\%x\d+', ' ', ingredients)
        # this would remove any non word chars, that is also punctuation
        # ingredients = re.sub('\W+', ' ', ingredients)
        return ingredients

    def get_instructions(self, recipe_index):
        instructions = self.db.get_instructions_for_index(recipe_index)
        instructions = re.sub(r'\%x\d+', ' ', instructions)
        # this would remove any non word chars, that is also punctuation
        # instructions = re.sub('\W+', ' ', instructions)
        return instructions

    def reset_made_recommendation_list(self):
        self.made_recommendations_list = []

    def get_details(self, recipe_index):
        # print("get_details in recommender: ", self.db.get_details_for_index(recipe_index))
        return self.db.get_details_for_index(recipe_index)

    def get_img_href(self, recipe_index):
        # print("get_img_href in recommender: ", self.db.get_img_href_for_index(recipe_index))
        return self.db.get_img_href_for_index(recipe_index)

    def get_similar_recipes(self, recipe_index):
        """
        :param : recipe_index needed to retrieve the current embedding from the embedding matrix to
                compute cosine-similarity with torch.topk for top score, no. of similar results k = 1
                - similarity with itself has been excluded by setting values of
                cos_score at index <=> already made recommendations to 0

        top_results looks like below:
        - values tensor contains the similarity scores
        - indices tensor contains the ids of the corresponding recipes

        torch.return_types.topk(
            values=tensor([1.0000, 0.8831, 0.8810, 0.8782, 0.8760, 0.8732, 0.8725, 0.8683, 0.8662, 0.8633]),
            indices=tensor([10, 168042, 293718, 108132, 263664, 31563, 219998, 176026, 283643, 133945])
            )

        :return: we need the 1st value from the indices' tensor: top_results[1][0], that is the index of the most
                similar recipe
        """
        cos_scores = util.pytorch_cos_sim(self.embeddings['embeddings'][recipe_index], self.embeddings['embeddings'])[0]
        cos_scores[self.made_recommendations_list] = 0
        print("cos_scores > 0.8 len: ", cos_scores[cos_scores > 0.9].shape)
        # top_results = torch.topk(cos_scores, k=C.NO_TOP_SIMILAR_RECIPES)
        # return top_results[1][0]
        similar_recipe_ids = (cos_scores > C.SIMILARITY_THRESHOLD).nonzero().squeeze().tolist()
        print("in recommender - similar_recipe_ids", len(similar_recipe_ids), similar_recipe_ids)
        similar_recipe_ids = list(set(similar_recipe_ids)-set(self.made_recommendations_list))
        print("in recommender - similar_recipe_ids - history", similar_recipe_ids)
        return similar_recipe_ids

    '''
    Alternative idea to simply start a new search when intent == get_Alternative + changes in preferences recognized 
    => pass the preferences together with the history of the ids and the similar recipes list to the DB to narrow down the results
     
    
        def get_similar_recommendation(self, similar_recipes_list, preferences):
        self.current_recommendation_index = self.db.get_recommendation(preferences,
                                                                       self.made_recommendations_list,
                                                                       similar_recipes_list)
        if self.current_recommendation_index is not None:
            # print("RECOMMENDER - get-recommendation: ", self.current_recommendation_index)
            self.made_recommendations_list.append(self.current_recommendation_index)
        return self.current_recommendation_index
    
    '''



    def add_index_to_history(self, index):
        self.made_recommendations_list.append(index)
