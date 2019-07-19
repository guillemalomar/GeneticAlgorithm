

class Environment:
    def __init__(self):
        self.tree_height = 1
        self.temperature = 20
        self.predators_speed = 10
        self.food_animals_speed = 10
        self.food_animals_strength = 1

    def create(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        return {
            "tree_height": self.tree_height,
            "temperature": self.temperature,
            "predators_speed": self.predators_speed,
            "food_animals_speed": self.food_animals_speed,
            "food_animals_strength": self.food_animals_strength
        }
