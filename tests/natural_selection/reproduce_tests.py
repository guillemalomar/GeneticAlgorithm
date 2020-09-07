import asyncio
import random
import unittest

from src.tools.database.data_wrapper import DataWrapper
from src.tools import set_db
from settings.settings import mutation_factor
from settings.human_model import HUMAN_PARAMS
from src.natural_selection.reproduce import obtain_children,\
    obtain_randomized_pairs,\
    obtain_pairs_of_individuals
from src import get_population_size


class ReproduceTests(unittest.TestCase):

    def test_obtain_randomized_individuals(self):
        my_indivs = obtain_randomized_pairs(int(get_population_size() * 0.6))
        self.assertEqual(len(my_indivs), int(get_population_size() * 0.3))
        for ind1, i in enumerate(my_indivs):
            for ind2, j in enumerate(my_indivs):
                if ind1 != ind2 and i == j:
                    raise Exception

    def test_obtain_randomized_pair_of_individuals(self):
        num_inds = 6000
        individuals = []
        for i in range(0, num_inds):
            indiv = {
                'height': 1,
                'arm_length': 2,
                'speed': 3,
                'strength': 4,
                'jump': 5,
                'skin_thickness': 6
            }
            individuals.append(indiv)
        curr_pop = {'bla_1_filtered': individuals}
        my_pairs = obtain_randomized_pairs(num_inds)
        new_indivs = obtain_pairs_of_individuals(curr_pop, my_pairs, 'bla_1_filtered')
        self.assertEquals(len(my_pairs), int(get_population_size() * 0.3))
        self.assertEquals(len(new_indivs), int(get_population_size() * 0.6))
        self.assertTrue('_id' in new_indivs[0])
        for pair in my_pairs:
            self.assertTrue(len(pair) == 2)

    def test_obtain_children(self):
        _ = asyncio.run(self.async_obtain_children(0, 1))

    async def async_obtain_children(self, indiv1_ind, indiv2_ind):
        set_db()
        rand_idx = random.randint(0, get_population_size())
        rand_iter = random.randint(0, get_population_size())

        indiv1_rand_height = random.uniform(HUMAN_PARAMS['height'][0],
                                            HUMAN_PARAMS['height'][1])
        indiv2_rand_height = random.uniform(HUMAN_PARAMS['height'][0],
                                            HUMAN_PARAMS['height'][1])
        indiv1_arm_length = random.uniform(HUMAN_PARAMS['arm_length'][0],
                                           HUMAN_PARAMS['arm_length'][1])
        indiv2_arm_length = random.uniform(HUMAN_PARAMS['arm_length'][0],
                                           HUMAN_PARAMS['arm_length'][1])
        indiv1_speed = random.uniform(HUMAN_PARAMS['speed'][0],
                                      HUMAN_PARAMS['speed'][1])
        indiv2_speed = random.uniform(HUMAN_PARAMS['speed'][0],
                                      HUMAN_PARAMS['speed'][1])
        indiv1_strength = random.uniform(HUMAN_PARAMS['strength'][0],
                                         HUMAN_PARAMS['strength'][1])
        indiv2_strength = random.uniform(HUMAN_PARAMS['strength'][0],
                                         HUMAN_PARAMS['strength'][1])
        indiv1_jump = random.uniform(HUMAN_PARAMS['jump'][0],
                                     HUMAN_PARAMS['jump'][1])
        indiv2_jump = random.uniform(HUMAN_PARAMS['jump'][0],
                                     HUMAN_PARAMS['jump'][1])
        indiv1_skin_thickness = random.uniform(HUMAN_PARAMS['skin_thickness'][0],
                                               HUMAN_PARAMS['skin_thickness'][1])
        indiv2_skin_thickness = random.uniform(HUMAN_PARAMS['skin_thickness'][0],
                                               HUMAN_PARAMS['skin_thickness'][1])
        indiv1 = {
            'height': indiv1_rand_height,
            'arm_length': indiv1_arm_length,
            'speed': indiv1_speed,
            'strength': indiv1_strength,
            'jump': indiv1_jump,
            'skin_thickness': indiv1_skin_thickness
        }

        indiv2 = {
            'height': indiv2_rand_height,
            'arm_length': indiv2_arm_length,
            'speed': indiv2_speed,
            'strength': indiv2_strength,
            'jump': indiv2_jump,
            'skin_thickness': indiv2_skin_thickness
        }
        current_population = DataWrapper()
        current_population["test_pop"] = [indiv1, indiv2]
        new_child = [
            asyncio.ensure_future(
                obtain_children(rand_idx, rand_iter, indiv1_ind, indiv2_ind, current_population, "test_pop")
            )
        ]
        _ = await asyncio.gather(*new_child)
        new_child = current_population["test_reproduction"][0]
        self.assertTrue(new_child['height'] > (indiv1['height'] + indiv2['height']) / 2 -
                        ((indiv1['height'] + indiv2['height']) * mutation_factor))
        self.assertTrue(new_child['height'] < (indiv1['height'] + indiv2['height']) / 2 +
                        ((indiv1['height'] + indiv2['height']) * mutation_factor))
        self.assertTrue(new_child['arm_length'] > (indiv1['arm_length'] + indiv2['arm_length']) / 2 -
                        ((indiv1['arm_length'] + indiv2['arm_length']) * mutation_factor))
        self.assertTrue(new_child['arm_length'] < (indiv1['arm_length'] + indiv2['arm_length']) / 2 +
                        ((indiv1['arm_length'] + indiv2['arm_length']) * mutation_factor))
        self.assertTrue(new_child['speed'] > (indiv1['speed'] + indiv2['speed']) / 2 -
                        ((indiv1['speed'] + indiv2['speed']) * mutation_factor))
        self.assertTrue(new_child['speed'] < (indiv1['speed'] + indiv2['speed']) / 2 +
                        ((indiv1['speed'] + indiv2['speed']) * mutation_factor))
        self.assertTrue(new_child['strength'] > (indiv1['strength'] + indiv2['strength']) / 2 -
                        ((indiv1['strength'] + indiv2['strength']) * mutation_factor))
        self.assertTrue(new_child['strength'] < (indiv1['strength'] + indiv2['strength']) / 2 +
                        ((indiv1['strength'] + indiv2['strength']) * mutation_factor))
        self.assertTrue(new_child['jump'] > (indiv1['jump'] + indiv2['jump']) / 2 -
                        ((indiv1['jump'] + indiv2['jump']) * mutation_factor))
        self.assertTrue(new_child['jump'] < (indiv1['jump'] + indiv2['jump']) / 2 +
                        ((indiv1['jump'] + indiv2['jump']) * mutation_factor))
        self.assertTrue(new_child['skin_thickness'] > (indiv1['skin_thickness'] + indiv2['skin_thickness']) / 2 -
                        ((indiv1['skin_thickness'] + indiv2['skin_thickness']) * mutation_factor))
        self.assertTrue(new_child['skin_thickness'] < (indiv1['skin_thickness'] + indiv2['skin_thickness']) / 2 +
                        ((indiv1['skin_thickness'] + indiv2['skin_thickness']) * mutation_factor))
        return 1
