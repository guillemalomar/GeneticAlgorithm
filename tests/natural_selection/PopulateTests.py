import random
import unittest

from src.natural_selection.populate import create_individuals, obtain_params
from settings.settings import initial_population_size


class PopulateTests(unittest.TestCase):

    def test_create_individuals(self):
        self.assertEquals(len(create_individuals('bla')), initial_population_size)

    def test_obtain_params(self):
        rand_int = random.randint(0, initial_population_size)
        result = obtain_params(rand_int)
        self.assertEquals(result['iteration'], 1)
        self.assertEquals(result['id'], rand_int)
        self.assertEquals(result['age'], int(rand_int / 2000) + 1)
