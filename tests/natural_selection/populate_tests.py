import random
import unittest

from src.natural_selection.populate import create_individuals, obtain_params
from settings.settings import initial_population_size


class PopulateTests(unittest.TestCase):

    def test_create_individuals(self):
        self.assertEqual(len(create_individuals('bla')), initial_population_size)

    def test_obtain_params(self):
        rand_int = random.randint(0, initial_population_size)
        result = obtain_params(rand_int)
        self.assertEqual(result['_id'], rand_int)
        self.assertEqual(result['age'], int(rand_int / int(initial_population_size / 5)) + 1)
