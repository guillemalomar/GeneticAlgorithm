

class Individual:
    def __init__(self):
        self.id = None
        self.iteration = None
        self.age = 0
        self.height = 0
        self.speed = 0
        self.jump = 0
        self.arm_length = 0
        self.skin_thickness = 0
        self.strength = 0

    def create(self, identifier=None, **kwargs):
        self.id = identifier
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_id(self, new_id):
        self.id = new_id

    def print_individual(self):
        print("####\nheight: {}\nspeed: {}\njump: {}\narm_length: {}\nstrength: {}\nreach: {}"
              .format(self.height,
                      self.speed,
                      self.jump,
                      self.arm_length,
                      self.strength,
                      self.height + self.jump + self.arm_length
                      ))


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
