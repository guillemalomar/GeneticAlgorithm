

class Environment:
    def __init__(self):
        self.fruit_tree_height = 0
        self.temperature = 0
        self.predators_speed = 0
        self.food_animals_speed = 0
        self.food_animals_strength = 0

    def create(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
