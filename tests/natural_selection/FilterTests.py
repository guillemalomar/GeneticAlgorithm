import random
import unittest

from src.model import Individual
from src.natural_selection.filter import filter_individuals, value_function, natural_death


class FilterTests(unittest.TestCase):

    def test_filter_individuals(self):
        population = []
        for i in range(0, 2050):
            ind = Individual()
            ind.set_height(i)
            population.append(ind)
        filtered_individuals = filter_individuals(population)
        self.assertEquals(len(filtered_individuals), 50)
        rand_pos = random.randint(0, 49)
        self.assertGreater(filtered_individuals[rand_pos+1].height, filtered_individuals[rand_pos].height)

    def test_filter(self):
        ind1 = Individual()
        self.assertEquals(type(value_function(ind1)), float)
        self.assertGreaterEqual(value_function(ind1), 0)

    def test_natural_death(self):
        population = []
        for i in range(1, 20):
            ind = Individual()
            ind.set_age(new_age=i % 5)
            population.append(ind)
        new_pop = natural_death(0, population)
        self.assertEquals(len(new_pop), 16)
