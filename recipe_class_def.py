class Recipe:
    def __init__(self, name, servings, preptime, cookingtime, difficulty, directions, ingredient_list):
        self.name = name
        self.servings = servings
        self.preptime = preptime
        self.cookingtime = cookingtime
        self.difficulty = difficulty
        self.directions = directions
        self.ingredient_list = ingredient_list
        self.recipe_id = -1
        self.image_file = None

    def generate_dict(self):
        data_in_dict = {}
        data_in_dict.update({"name": self.name})
        data_in_dict.update({"servings": self.servings})
        data_in_dict.update({"preptime": self.preptime})
        data_in_dict.update({"cookingtime": self.cookingtime})
        data_in_dict.update({"difficulty": self.difficulty})
        data_in_dict.update({"directions": self.directions})
        data_in_dict.update({"ingredient_list": self.ingredient_list})
        data_in_dict.update({"recipe_id": self.recipe_id})
        data_in_dict.update({"image_file": self.image_file})
        return data_in_dict
