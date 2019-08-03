import random
import unittest

from src.natural_selection.filter import filter_individuals, human_value_function
from src.environment import Environment
from src import get_population_size
from src.tools.data_wrapper import DataWrapper
from src.tools import set_db


class FilterTests(unittest.TestCase):

    def test_filter_individuals(self):
        set_db("To define")
        environment_params = {
            'tree_height': 1.0,
            'temperature': 20.0,
            'predators_speed': 10.0,
            'food_animals_speed': 10.0,
            'food_animals_strength': 1.0
        }
        environment = Environment('Bla', environment_params)
        population = DataWrapper("To define")
        collection = []
        for i in range(0, get_population_size() + 50):
            ind = {
                'height': 1,
                'arm_length': 0,
                'speed': 10,
                'strength': i,
                'jump': 0,
                'skin_thickness': 0.05,
                'total_reach': 2
            }
            collection.append(ind)
        population['Bla_1'] = collection
        filtered_individuals = filter_individuals(population, environment, 1)
        self.assertEqual(len(filtered_individuals['Bla_1_filtered']), int(get_population_size() * 0.6))
        rand_pos = random.randint(0, 49)
        self.assertGreater(filtered_individuals['Bla_1'][rand_pos+1]['strength'],
                           filtered_individuals['Bla_1'][rand_pos]['strength'])

    def test_filter(self):
        environment = {
            'tree_height': 1.0,
            'temperature': 20.0,
            'predators_speed': 10.0,
            'food_animals_speed': 10.0,
            'food_animals_strength': 1.0
        }
        ind = {
            'height': 1,
            'arm_length': 0,
            'speed': 10,
            'strength': 1,
            'jump': 0,
            'skin_thickness': 0.05,
            'total_reach': 2
        }
        self.assertEqual(type(human_value_function(ind, environment)), float)
        self.assertGreaterEqual(human_value_function(ind, environment), 0)
