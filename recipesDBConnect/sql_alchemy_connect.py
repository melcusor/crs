from config.config import KochbarConfig as Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from sqlalchemy import Column, Integer, String, or_, Float, Text, and_
import sqlalchemy as db

RECIPES_TABLE_NAME = 'recipes'
RECIPES_LABELS_COLUMN = 'category_label'
RECIPES_CLEAN_INGREDIENTS_COLUMN = 'cleaned_ingredients'
RECIPES_CLEAN_TITLES_COLUMN = 'cleaned_title'

RECIPES_IMG_HREF_COLUMN = 'img_href'

RECIPES_SERVINGS_COLUMN = 'no_servings'
RECIPES_DIFFICULTY_COLUMN = 'difficulty'
RECIPES_DURATION_COLUMN = 'duration'
RECIPES_KJ_COLUMN = 'kj'
RECIPES_KCAL_COLUMN = 'kcal'
RECIPES_RAW_TITLES_COLUMN = 'title'
RECIPES_RAW_INGREDIENTS_COLUMN = 'raw_ingredients'
RECIPES_RAW_INSTRUCTIONS_COLUMN = 'raw_instructions'

RECIPES_INDEX_COLUMN = 'index'

# needed because during the cleaning process of the recipe titles umlaute were transformed, eg. "Äpfel" => "aepfel"
SPECIAL_CHAR_MAP = {ord('ä'): 'ae',
                    ord('ü'): 'ue',
                    ord('ö'): 'oe',
                    ord('ß'): 'ss'}


def _connect_to_sql_db():
    try:
        # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
        engine = db.create_engine(
            # url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            url="mysql://{0}:{1}@{2}:{3}/{4}".format(
                Config.USER, Config.PASSWORD, Config.HOST, Config.PORT, Config.DATABASE
                # USER, PASSWORD, HOST, PORT, DATABASE
            )
        )
        print(f"Connection to the {Config.HOST} for user {Config.USER} created successfully.")
        # print(f"Connection to the {HOST} for user {USER} created successfully.")
    except Exception as ex:
        print("\n+++\n")
        print("Connection could not be made due to the following error: \n", ex)
        print("\n+++\n")

    return engine


def _query_db(queries):
    result = None
    try:
        ##################################################################################
        session = KochbarDB.Session()
        result = session.query(KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_INDEX_COLUMN])
        # result = KochbarDB.session.query(KochbarDB.metadata.tables[RECIPES_TABLE_NAME])

        # result = result.filter(*queries).limit(1000).all()
        result = result.filter(*queries).order_by(func.rand()).limit(50).all()
        # result = result.filter(*queries).order_by(func.rand()).first()

        # commit is optional here, because we only read data from the db
        # session.commit()

    except Exception as ex:
        session.rollback()
        print("1. Querying recipe table returned an error: \n", ex)
        raise
    finally:
        session.close()
    return result


class KochbarDB(object):
    engine = _connect_to_sql_db()
    base = declarative_base(engine)
    metadata = base.metadata

    Session = sessionmaker(bind=engine)

    @staticmethod
    def get_recommendation(preferences, made_recommendations_list, similar_recipes_idx_list):
        print("DB - Already made recommendations: ", made_recommendations_list)
        print("get_recommendation method - preferences: ", preferences)
        if similar_recipes_idx_list:
            print("DB - There is a list of indices of similar recipes: ", similar_recipes_idx_list)
        else:
            print("DB - No list of similar recipes")
        ####################################################################
        # get recipe_title (in and out) options as lists of separated tokens
        # one title can contain several 1 and more tokens
        recipe_title_in = ' '.join(
            [token.translate(SPECIAL_CHAR_MAP) for token in preferences["recipe_title"]["entities_in"]])
        recipe_title_in = recipe_title_in.split()

        recipe_title_out = ' '.join(
            [token.translate(SPECIAL_CHAR_MAP) for token in preferences["recipe_title"]["entities_out"]])
        recipe_title_out = recipe_title_out.split()

        print("RECIPE TITLE IN: ", recipe_title_in)
        print("RECIPE TITLE OUT: ", recipe_title_out)

        ##########################################################################################################
        # get labels (in and out) options as 2 lists of separated tokens: menu, prep_method, occasion, dish_type etc.
        labels_in = []
        labels_out = []
        for key, value in preferences.items():
            if key not in ["recipe_title", "ingredients"]:
                current_label_in = preferences[key]["entities_in"]
                current_label_out = preferences[key]["entities_out"]

                if current_label_in:
                    labels_in = labels_in + current_label_in
                if current_label_out:
                    labels_out = labels_out + current_label_out

        print("LABELS_IN - LIST: ", labels_in)
        print("LABELS_OUT - LIST: ", labels_out)

        ####################################################################
        # get ingredients (in and out) options as lists of separated tokens
        ingredients_in = preferences["ingredients"]["entities_in"]
        ingredients_out = preferences["ingredients"]["entities_out"]

        print("INGRED_IN: ", ingredients_in)
        print("INGRED_OUT: ", ingredients_out)

        # https://stackoverflow.com/questions/31063860/conditionally-filtering-in-sqlalchemy
        queries = []
        # THE "OUT" PREFERENCES ARE NOT SEEN AS OPTIONAL, BUT RATHER AS IMPERATIVE => WILL ALWAYS BE CONSIDERED
        # IN THE 1ST RUN: CONSIDER ALL ELICITED PREFERENCES WHEN FILTERING RESULTS

        if similar_recipes_idx_list:
            queries.append(or_(KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_INDEX_COLUMN] == v for v in
                               similar_recipes_idx_list))
        if recipe_title_in:
            print("sql_alchemy_connect, recipe_title_in IN query")
            queries.append(and_(
                KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_CLEAN_TITLES_COLUMN].ilike(f'%{v}%') for v
                in recipe_title_in))
            if recipe_title_out:
                queries.append(and_(
                    KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_CLEAN_TITLES_COLUMN].notilike(
                        f'%{v}%') for v in recipe_title_out))
            if ingredients_in:
                queries.append(and_(
                    KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_CLEAN_INGREDIENTS_COLUMN].ilike(
                        f'%{v}%') for v in ingredients_in))
            if ingredients_out:
                queries.append(and_(
                    KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_CLEAN_INGREDIENTS_COLUMN].notilike(
                        f'%{v}%') for v in ingredients_out))
            if labels_in:
                queries.append(and_(
                    KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_LABELS_COLUMN].ilike(f'%{v}%') for v
                    in labels_in))
            if labels_out:
                queries.append(and_(
                    KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_LABELS_COLUMN].notilike(f'%{v}%') for
                    v in labels_out))
            if made_recommendations_list:
                queries.append(and_(
                    KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_INDEX_COLUMN] != v for v in
                    made_recommendations_list))

            result = _query_db(queries)
            if result is None:
                # In this query we do not consider labels_in
                queries = [and_(
                    KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_CLEAN_TITLES_COLUMN].ilike(f'%{v}%')
                    for v in recipe_title_in)]
                if ingredients_in:
                    queries.append(and_(
                        KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_CLEAN_INGREDIENTS_COLUMN].ilike(
                            f'%{v}%') for v in ingredients_in))
                if ingredients_out:
                    queries.append(and_(
                        KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[
                            RECIPES_CLEAN_INGREDIENTS_COLUMN].notilike(
                            f'%{v}%') for v in ingredients_out))
                if labels_out:
                    queries.append(and_(
                        KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_LABELS_COLUMN].notilike(f'%{v}%')
                        for
                        v in labels_out))
                if made_recommendations_list:
                    queries.append(and_(
                        KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_INDEX_COLUMN] != v for v in
                        made_recommendations_list))
                result = _query_db(queries)
                if result is None:
                    # in this query we do not consider ingredients_in
                    queries = [and_(
                        KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_CLEAN_TITLES_COLUMN].ilike(
                            f'%{v}%')
                        for v in recipe_title_in)]
                    if ingredients_out:
                        queries.append(and_(
                            KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[
                                RECIPES_CLEAN_INGREDIENTS_COLUMN].notilike(
                                f'%{v}%') for v in ingredients_out))
                    if labels_in:
                        queries.append(and_(
                            KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_LABELS_COLUMN].ilike(
                                f'%{v}%') for
                            v in labels_in))
                    if labels_out:
                        queries.append(and_(
                            KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_LABELS_COLUMN].notilike(
                                f'%{v}%') for
                            v in labels_out))
                    if made_recommendations_list:
                        queries.append(and_(
                            KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_INDEX_COLUMN] != v for v in
                            made_recommendations_list))
                    result = _query_db(queries)
        ################################################################################################################
        ################################################################################################################

        # 2ND RUN: IF RESULT IS NONE, CHECK WHETHER RECIPE TITLE IN PREFERENCES
        # IF SO, ADD ONLY INGREDIENTS FILTER TO QUERY, BECAUSE LABELS ARE NOT ALWAYS COMPLETE [AND RELIABLE?]
        else:
            print("sql_alchemy_connect, recipe_title_in NOT query")
            # we consider all 4 in and out for labels and ingredients
            queries = []
            # if recipe_title_out:
            #     queries.append(or_(
            #         KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_CLEAN_TITLES_COLUMN].notilike(
            #             f'%{v}%') for v in recipe_title_out))
            if similar_recipes_idx_list:
                queries.append(
                    or_(KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_INDEX_COLUMN] == v for v in
                        similar_recipes_idx_list))
            if ingredients_in:
                queries.append(and_(
                    KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[
                        RECIPES_CLEAN_INGREDIENTS_COLUMN].ilike(
                        f'%{v}%') for v in ingredients_in))
            if ingredients_out:
                queries.append(and_(
                    KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[
                        RECIPES_CLEAN_INGREDIENTS_COLUMN].notilike(
                        f'%{v}%') for v in ingredients_out))
            if labels_in:
                queries.append(and_(
                    KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_LABELS_COLUMN].ilike(f'%{v}%') for v
                    in labels_in))
            if labels_out:
                queries.append(and_(
                    KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_LABELS_COLUMN].notilike(
                        f'%{v}%')
                    for v in labels_out))
            if made_recommendations_list:
                queries.append(and_(
                    KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_INDEX_COLUMN] != v for v in
                    made_recommendations_list))
            result = _query_db(queries)
            if result is None:
                print("")
                queries = []
                if ingredients_out:
                    queries.append(and_(
                        KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[
                            RECIPES_CLEAN_INGREDIENTS_COLUMN].notilike(
                            f'%{v}%') for v in ingredients_out))
                if labels_in:
                    queries.append(and_(
                        KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_LABELS_COLUMN].ilike(f'%{v}%') for
                        v
                        in labels_in))
                if labels_out:
                    queries.append(and_(
                        KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_LABELS_COLUMN].notilike(
                            f'%{v}%')
                        for v in labels_out))
                result = _query_db(queries)
                if result is None:
                    queries = []
                    if ingredients_in:
                        queries.append(and_(
                            KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_LABELS_COLUMN].ilike(f'%{v}%')
                            for
                            v
                            in ingredients_in))
                    if ingredients_out:
                        queries.append(and_(
                            KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[
                                RECIPES_CLEAN_INGREDIENTS_COLUMN].notilike(
                                f'%{v}%') for v in ingredients_out))
                    if labels_out:
                        queries.append(and_(
                            KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_LABELS_COLUMN].notilike(
                                f'%{v}%')
                            for v in labels_out))
                    result = _query_db(queries)


            # print("get_recommendation method - result: ", type(result), result, result[0])
            # result = result.filter(*queries).order_by(func.rand()).limit(5).all()
            # result = [x[0] for x in result]

        # if result is still none => sorry, no results for your preferences
        print("SQL ALCHEMY RECOMMENDATION - end result: ", result)

        if result is None or result == []:
            return None
        else:
            return result[0][0]

    @staticmethod
    def get_title_for_index(recipe_index):
        result = None
        session = KochbarDB.Session()

        try:
            result = session.query(
                KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_RAW_TITLES_COLUMN]).filter(
                KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_INDEX_COLUMN] == recipe_index).first()

            # session.commit()
        except Exception as ex:
            session.rollback()
            print("Querying recipe table for title returned an error: \n", ex)
            raise
        finally:
            session.close()

        return result[0]

    @staticmethod
    def get_ingredients_for_index(recipe_index):
        result = None
        session = KochbarDB.Session()

        try:
            result = session.query(
                KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_RAW_INGREDIENTS_COLUMN]).filter(
                KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_INDEX_COLUMN] == recipe_index).first()

            # session.commit()
        except Exception as ex:
            session.rollback()
            print("Querying recipe table for ingredients returned an error: \n", ex)
            raise
        finally:
            session.close()
        print("get_ingredients_for_index - result: ", result)
        return result[0]

    @staticmethod
    def get_instructions_for_index(recipe_index):
        result = None
        session = KochbarDB.Session()

        try:
            result = session.query(
                KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_RAW_INSTRUCTIONS_COLUMN]).filter(
                KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_INDEX_COLUMN] == recipe_index).first()

            # session.commit()
        except Exception as ex:
            session.rollback()
            print("Querying recipe table for instructions returned an error: \n", ex)
            raise
        finally:
            session.close()
        print("get_instructions_for_index - result: ", result)

        return result[0]

    @staticmethod
    def get_details_for_index(recipe_index):
        result = None
        session = KochbarDB.Session()

        try:
            result = session.query(KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns["no_servings"],
                                   KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns["duration"],
                                   KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns["difficulty"],
                                   KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns["kj"],
                                   KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns["kcal"],
                                   KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns["protein"],
                                   KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns["carbohydrates"],
                                   KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns["fat"]).filter(
                KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_INDEX_COLUMN] == recipe_index).first()

            # session.commit()
        except Exception as ex:
            session.rollback()
            print("Querying recipe table for details returned an error: \n", ex)
            raise
        finally:
            session.close()
        print("get_details_for_index - result: ", result)

        details = None
        if result:
            details = {
                "no_servings": result[0],
                "duration": result[1],
                "difficulty": result[2],
                "kj": result[3],
                "kcal": result[4],
                "protein": result[5],
                "carbohydrates": result[6],
                "fat": result[7]
            }

        return details

    @staticmethod
    def get_img_href_for_index(recipe_index):
        result = None
        session = KochbarDB.Session()

        try:
            result = session.query(
                KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_IMG_HREF_COLUMN]).filter(
                KochbarDB.metadata.tables[RECIPES_TABLE_NAME].columns[RECIPES_INDEX_COLUMN] == recipe_index).first()

            # session.commit()
        except Exception as ex:
            session.rollback()
            print("Querying recipe table for details returned an error: \n", ex)
            raise
        finally:
            session.close()
        print("get_details_for_index - result: ", result)

        return result[0]

    @staticmethod
    def sql_check_ne(token, table, column):

        session = KochbarDB.Session()
        try:
            result = session.query(KochbarDB.metadata.tables[table]).filter(
                KochbarDB.metadata.tables[table].columns[column].ilike(f'{token}')).first()

            session.commit()
        except Exception as ex:
            session.rollback()
            print("Query check for NEs returned an error: \n", ex)
            raise
        finally:
            session.close()
        # print("SQL CHECK NE: ", token, table, column, " => ", result)
        return result

    class Ingredients(base):
        __tablename__ = 'ingredients'
        __table_args__ = {'autoload': True}

        index = Column(Integer)
        ingredient = Column(String(128), primary_key=True, nullable=False)
        top_cats = Column(String(128), nullable=False)
        sub_cats = Column(String(128), nullable=False)
        syns = Column(String(128), nullable=False)

    class Cuisine(base):
        __tablename__ = 'cuisine'
        __table_args__ = {'autoload': True}

        index = Column(Integer)
        cuisine = Column(String(128), primary_key=True, nullable=False)
        # syns = Column(String(128), nullable=False)

    class DietHealthy(base):
        __tablename__ = 'diet_healthy'
        __table_args__ = {'autoload': True}

        index = Column(Integer)
        diet_healthy_category = Column(String(128), primary_key=True, nullable=False)

    class DishType(base):
        __tablename__ = 'dish_type'
        __table_args__ = {'autoload': True}

        index = Column(Integer)
        dish_type = Column(String(128), primary_key=True, nullable=False)
        # syns = Column(String(128), nullable=False)

    class Menu(base):
        __tablename__ = 'menu'
        __table_args__ = {'autoload': True}

        index = Column(Integer)
        menu = Column(String(128), primary_key=True, nullable=False)
        # syns = Column(String(128), nullable=False)

    class Occasion(base):
        __tablename__ = 'occasion'
        __table_args__ = {'autoload': True}

        index = Column(Integer)
        occasion = Column(String(128), primary_key=True, nullable=False)
        # syns = Column(String(128), nullable=False)

    class PreparationMethod(base):
        __tablename__ = 'preparation_method'
        __table_args__ = {'autoload': True}

        index = Column(Integer)
        preparation_method = Column(String(128), primary_key=True, nullable=False)
        # syns = Column(String(128), nullable=False)

    class Recipes(base):
        __tablename__ = 'recipes'
        __table_args__ = {'autoload': True}

        index = Column(Integer)
        id = Column(Integer)
        recipe_href = Column(String(128), primary_key=True, nullable=False)
        title = Column(String(128))
        cleaned_title = Column(String(128))
        no_ratings = Column(Integer)
        no_favorites = Column(Integer)
        no_views = Column(Integer)
        no_servings = Column(Integer)
        difficulty = Column(String(8))
        duration = Column(Float)
        kj = Column(Integer)
        kcal = Column(Integer)
        protein = Column(Float)
        carbohydrates = Column(Float)
        fat = Column(Float)
        raw_ingredients = Column(Text)
        cleaned_ingredients = Column(Text)
        raw_instructions = Column(Text)
        category_label = Column(Text)
        cleaned_instructions = Column(Text)
        img_href = Column(Text)
