import random
import unittest

from src.natural_selection.populate import create_individuals, obtain_params
from src import get_population_size
from src.tools import set_db


class PopulateTests(unittest.TestCase):

    def test_create_individuals(self):
        set_db()
        self.assertEqual(len(create_individuals('bla')['bla_1']), get_population_size())

    def test_obtain_params(self):
        rand_int = random.randint(0, get_population_size())
        result = obtain_params(rand_int)
        self.assertEqual(result['_id'], rand_int)
        self.assertEqual(result['age'], int(rand_int / int(get_population_size() / 5)) + 1)
