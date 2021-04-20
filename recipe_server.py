import json
import sqlite3
from sqlite3 import Error
import flask
from ingredient_class_def import Ingredient
from recipe_class_def import Recipe
from flask import request, jsonify


databaseName = "recipe"
create_table_ingredient_sql = """CREATE TABLE IF NOT EXISTS ingredient (
                        id integer primary key autoincrement,
                        ingredient text,
                        amount  integer,
                        unit text,
                        recipe_id integer,
                        foreign key (recipe_id) references recipe(recipe_id)
                        );"""

create_table_recipe_sql = """CREATE TABLE IF NOT EXISTS recipe (
                        recipe_id integer primary key autoincrement,
                        name text,
                        servings  integer,
                        prep_time real,
                        cooking_time real,
                        difficulty text,
                        directions text,
                        image_file text
                        );"""


def init_connection():
    """
    creates connection to database
    :return: connection object
    """
    try:
        conn = None
        conn = sqlite3.connect(databaseName)
        return conn
    except Error:
        print(Error)


def create_table(connection, sql_statement):
    """
    Creates tables for stock data
    :param connection: connection object
    :param sql_statement: sql statement to execute
    :return: none
    """
    try:
        query = connection.cursor()
        query.execute(sql_statement)
    except Error:
        print(Error)


def create_database():
    conn = init_connection()
    create_table(conn, create_table_recipe_sql)
    create_table(conn, create_table_ingredient_sql)
    conn.close()


if __name__ == '__main__':
    myapp = flask.Flask(__name__)
    myapp.config['DEBUG'] = True


    @myapp.route("/recipes", methods=['GET'])
    def get_all_recipes():
        conn_recipe = init_connection()
        conn_ingredient = init_connection()
        recipe_list = []
        ingredient_list = []
        data_cursor_recipe = conn_recipe.cursor()
        data_cursor_ingredient = conn_ingredient.cursor()

        result_recipe = data_cursor_recipe.execute("SELECT recipe_id, "
                                     "name, "
                                     "servings, "
                                     "prep_time, "
                                     "cooking_time, "
                                     "difficulty, "
                                     "directions, "
                                     "image_file "
                                     "FROM recipe;").fetchall()

        for rec in result_recipe:

            ingredient_sql = "SELECT ingredient, amount, unit FROM ingredient where recipe_id="
            ingredient_sql = ingredient_sql + str(rec[0])

            result_ingredient = data_cursor_ingredient.execute(ingredient_sql).fetchall()

            for ing in result_ingredient:
                ingredient = Ingredient(ing[0], ing[1], ing[2])
                ingredient_list.append(ingredient.generate_dict())

            recipe = Recipe(rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], ingredient_list)
            recipe.recipe_id = rec[0]
            recipe.image_file = rec[7]
            recipe_list.append(recipe.generate_dict())

        conn_recipe.close()
        conn_ingredient.close()
        """
        :return recipe_list
        """
        return jsonify(recipe_list)

    @myapp.route("/addrecipe", methods=['post'])
    def add_recipe():
        record = json.loads(request.data)
        conn = init_connection()
        data_cursor = conn.cursor()
        data_to_save = [record["name"], record["servings"], record["preptime"],
                        record["cookingtime"], record["difficulty"], record["directions"],
                        record["image_file"]]

        data_cursor.execute("INSERT INTO recipe "
                            "(name, servings, prep_time, cooking_time, difficulty, directions, image_file)"
                            " VALUES (?, ?, ?, ?, ?,?, ?);", data_to_save)

        conn.commit()

        for x in record["ingredient_list"]:
            ingredient = [x["ingredient"], x["amount"], x["units"], data_cursor.lastrowid]
            data_cursor.execute("INSERT INTO ingredient (ingredient, amount, unit, recipe_id) "
                                "VALUES (?, ?, ?, ?)", ingredient)
            conn.commit()
        conn.close()
        return jsonify({"response": "valid"})

    @myapp.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        header["Access-Control-Allow-Headers"] = '*'
        return response

    myapp.run()
