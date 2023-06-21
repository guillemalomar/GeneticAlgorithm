import unittest

from src.natural_selection.natural_death import natural_death
from src import get_population_size
from src.tools.database.data_wrapper import DataWrapper
from src.tools import set_db


class NaturalDeathTests(unittest.TestCase):

    def test_natural_death(self):
        set_db()
        population = DataWrapper()
        collection = []
        for i in range(0, get_population_size() + 100):
            ind = {
                "age": i % 5,
                "height": 1,
                "arm_length": 0,
                "speed": 10,
                "strength": 1,
                "jump": 0,
                "skin_thickness": 0.05
            }
            collection.append(ind)
        population["Bla_1_reproduction"] = collection
        new_pop = natural_death(1, population, "Bla")
        self.assertEqual(len(new_pop["Bla_2"]), get_population_size())
