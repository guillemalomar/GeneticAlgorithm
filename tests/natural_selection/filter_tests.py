import random
import unittest

from src.natural_selection.filter import filter_individuals, human_value_function
from src.natural_selection.natural_death import natural_death
from settings.settings import initial_population_size


class FilterTests(unittest.TestCase):

    def test_filter_individuals(self):
        environment = {
            'tree_height': 1.0,
            'temperature': 20.0,
            'predators_speed': 10.0,
            'food_animals_speed': 10.0,
            'food_animals_strength': 1.0
        }
        population = []
        for i in range(0, initial_population_size + 50):
            ind = {
                'height': 1,
                'arm_length': 0,
                'speed': 10,
                'strength': i,
                'jump': 0,
                'skin_thickness': 0.05,
                'total_reach': 2
            }
            population.append(ind)
        filtered_individuals = filter_individuals(population, environment)
        self.assertEqual(len(filtered_individuals), int(initial_population_size * 0.6))
        rand_pos = random.randint(0, 49)
        self.assertGreater(filtered_individuals[rand_pos+1]['strength'],
                           filtered_individuals[rand_pos]['strength'])

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

    def test_natural_death(self):
        population = []
        for i in range(0, initial_population_size + 1000):
            ind = {
                'age': i % 5,
                'height': 1,
                'arm_length': 0,
                'speed': 10,
                'strength': 1,
                'jump': 0,
                'skin_thickness': 0.05
            }
            population.append(ind)
        new_pop = natural_death(0, population)
        self.assertEqual(len(new_pop), initial_population_size)
