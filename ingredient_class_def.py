class Ingredient:
    def __init__(self, ingredient, amount, units):
        self.ingredient = ingredient
        self.amount = amount
        self.units = units

    def generate_dict(self):
        data = {}
        data.update({"ingredient": self.ingredient})
        data.update({"amount": self.amount})
        data.update({"units": self.units})
        return data
