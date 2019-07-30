import asyncio
import random
import unittest

from settings.settings import initial_population_size, INDIVIDUALS_PARAMS, mutation_factor
from src.natural_selection.reproduce import obtain_children,\
    obtain_randomized_pairs,\
    obtain_randomized_pairs_of_individuals


class ReproduceTests(unittest.TestCase):

    def test_obtain_randomized_individuals(self):
        my_indivs = obtain_randomized_pairs(6000)
        self.assertEqual(len(my_indivs), 3000)
        for ind1, i in enumerate(my_indivs):
            for ind2, j in enumerate(my_indivs):
                if ind1 != ind2 and i == j:
                    raise Exception

    def test_obtain_randomized_pair_of_individuals(self):
        num_inds = 6000
        curr_pop = []
        for i in range(0, num_inds):
            indiv = {
                'height': 1,
                'arm_length': 2,
                'speed': 3,
                'strength': 4,
                'jump': 5,
                'skin_thickness': 6
            }
            curr_pop.append(indiv)
        my_pairs = obtain_randomized_pairs(num_inds)
        new_indivs = obtain_randomized_pairs_of_individuals(curr_pop, my_pairs)
        self.assertEquals(len(my_pairs), 3000)
        self.assertEquals(len(new_indivs), 6000)
        self.assertTrue('_id' in new_indivs[0])
        for pair in my_pairs:
            self.assertTrue(len(pair) == 2)

    def test_obtain_children(self):
        _ = asyncio.run(self.async_obtain_children(0, 1))

    async def async_obtain_children(self, indiv1_ind, indiv2_ind):
        rand_idx = random.randint(0, initial_population_size)
        rand_iter = random.randint(0, initial_population_size)

        indiv1_rand_height = random.uniform(INDIVIDUALS_PARAMS['height'][0],
                                            INDIVIDUALS_PARAMS['height'][1])
        indiv2_rand_height = random.uniform(INDIVIDUALS_PARAMS['height'][0],
                                            INDIVIDUALS_PARAMS['height'][1])
        indiv1_arm_length = random.uniform(INDIVIDUALS_PARAMS['arm_length'][0],
                                           INDIVIDUALS_PARAMS['arm_length'][1])
        indiv2_arm_length = random.uniform(INDIVIDUALS_PARAMS['arm_length'][0],
                                           INDIVIDUALS_PARAMS['arm_length'][1])
        indiv1_speed = random.uniform(INDIVIDUALS_PARAMS['speed'][0],
                                      INDIVIDUALS_PARAMS['speed'][1])
        indiv2_speed = random.uniform(INDIVIDUALS_PARAMS['speed'][0],
                                      INDIVIDUALS_PARAMS['speed'][1])
        indiv1_strength = random.uniform(INDIVIDUALS_PARAMS['strength'][0],
                                         INDIVIDUALS_PARAMS['strength'][1])
        indiv2_strength = random.uniform(INDIVIDUALS_PARAMS['strength'][0],
                                         INDIVIDUALS_PARAMS['strength'][1])
        indiv1_jump = random.uniform(INDIVIDUALS_PARAMS['jump'][0],
                                     INDIVIDUALS_PARAMS['jump'][1])
        indiv2_jump = random.uniform(INDIVIDUALS_PARAMS['jump'][0],
                                     INDIVIDUALS_PARAMS['jump'][1])
        indiv1_skin_thickness = random.uniform(INDIVIDUALS_PARAMS['skin_thickness'][0],
                                               INDIVIDUALS_PARAMS['skin_thickness'][1])
        indiv2_skin_thickness = random.uniform(INDIVIDUALS_PARAMS['skin_thickness'][0],
                                               INDIVIDUALS_PARAMS['skin_thickness'][1])
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
        current_population = [indiv1, indiv2]
        new_child = [
            asyncio.ensure_future(obtain_children(rand_idx, rand_iter, indiv1_ind, indiv2_ind, current_population))
        ]
        response = await asyncio.gather(*new_child)
        new_child = response[0]
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
        return response[0]
