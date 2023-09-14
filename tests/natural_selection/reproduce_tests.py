import asyncio
import random
import unittest

from src.tools.database.data_wrapper import DataWrapper
from src.tools import set_db
from settings.settings import mutation_factor
from settings.human_model import HUMAN_PARAMS
from src.natural_selection.reproduce import obtain_children, \
    obtain_randomized_pairs, \
    obtain_pairs_of_individuals
from src import get_population_size


class ReproduceTests(unittest.TestCase):

    def test_obtain_randomized_individuals(self):
        my_individuals = obtain_randomized_pairs(int(get_population_size() * 0.6))
        self.assertEqual(len(my_individuals), int(get_population_size() * 0.3))
        for ind1, i in enumerate(my_individuals):
            for ind2, j in enumerate(my_individuals):
                if ind1 != ind2 and i == j:
                    raise Exception

    def test_obtain_randomized_pair_of_individuals(self):
        num_individuals = 6000
        individuals = []
        for i in range(0, num_individuals):
            individual = {
                "height": 1,
                "arm_length": 2,
                "speed": 3,
                "strength": 4,
                "jump": 5,
                "skin_thickness": 6
            }
            individuals.append(individual)
        current_population = {"bla_1_filtered": individuals}
        my_pairs = obtain_randomized_pairs(num_individuals)
        new_individuals = obtain_pairs_of_individuals(current_population, my_pairs, "bla_1_filtered")
        self.assertEquals(len(my_pairs), int(get_population_size() * 0.3))
        self.assertEquals(len(new_individuals), int(get_population_size() * 0.6))
        self.assertTrue("_id" in new_individuals[0])
        for pair in my_pairs:
            self.assertTrue(len(pair) == 2)

    def test_obtain_children(self):
        _ = asyncio.run(self.async_obtain_children(0, 1))

    async def async_obtain_children(self, individual1_ind, individual2_ind):
        set_db()
        rand_idx = random.randint(0, get_population_size())
        rand_iter = random.randint(0, get_population_size())

        individual1_rand_height = random.uniform(HUMAN_PARAMS["height"][0],
                                                 HUMAN_PARAMS["height"][1])
        individual2_rand_height = random.uniform(HUMAN_PARAMS["height"][0],
                                                 HUMAN_PARAMS["height"][1])
        individual1_arm_length = random.uniform(HUMAN_PARAMS["arm_length"][0],
                                                HUMAN_PARAMS["arm_length"][1])
        individual2_arm_length = random.uniform(HUMAN_PARAMS["arm_length"][0],
                                                HUMAN_PARAMS["arm_length"][1])
        individual1_speed = random.uniform(HUMAN_PARAMS["speed"][0],
                                           HUMAN_PARAMS["speed"][1])
        individual2_speed = random.uniform(HUMAN_PARAMS["speed"][0],
                                           HUMAN_PARAMS["speed"][1])
        individual1_strength = random.uniform(HUMAN_PARAMS["strength"][0],
                                              HUMAN_PARAMS["strength"][1])
        individual2_strength = random.uniform(HUMAN_PARAMS["strength"][0],
                                              HUMAN_PARAMS["strength"][1])
        individual1_jump = random.uniform(HUMAN_PARAMS["jump"][0],
                                          HUMAN_PARAMS["jump"][1])
        individual2_jump = random.uniform(HUMAN_PARAMS["jump"][0],
                                          HUMAN_PARAMS["jump"][1])
        individual1_skin_thickness = random.uniform(HUMAN_PARAMS["skin_thickness"][0],
                                                    HUMAN_PARAMS["skin_thickness"][1])
        individual2_skin_thickness = random.uniform(HUMAN_PARAMS["skin_thickness"][0],
                                                    HUMAN_PARAMS["skin_thickness"][1])
        individual1 = {
            "height": individual1_rand_height,
            "arm_length": individual1_arm_length,
            "speed": individual1_speed,
            "strength": individual1_strength,
            "jump": individual1_jump,
            "skin_thickness": individual1_skin_thickness
        }

        individual2 = {
            "height": individual2_rand_height,
            "arm_length": individual2_arm_length,
            "speed": individual2_speed,
            "strength": individual2_strength,
            "jump": individual2_jump,
            "skin_thickness": individual2_skin_thickness
        }
        current_population = DataWrapper()
        current_population["test_pop"] = [individual1, individual2]
        new_child = [
            asyncio.ensure_future(
                obtain_children(rand_idx, rand_iter, individual1_ind, individual2_ind, current_population, "test_pop")
            )
        ]
        _ = await asyncio.gather(*new_child)
        new_child = current_population["test_reproduction"][0]
        self.assertTrue(new_child["height"] > (individual1["height"] + individual2["height"]) / 2 -
                        ((individual1["height"] + individual2["height"]) * mutation_factor))
        self.assertTrue(new_child["height"] < (individual1["height"] + individual2["height"]) / 2 +
                        ((individual1["height"] + individual2["height"]) * mutation_factor))
        self.assertTrue(new_child["arm_length"] > (individual1["arm_length"] + individual2["arm_length"]) / 2 -
                        ((individual1["arm_length"] + individual2["arm_length"]) * mutation_factor))
        self.assertTrue(new_child["arm_length"] < (individual1["arm_length"] + individual2["arm_length"]) / 2 +
                        ((individual1["arm_length"] + individual2["arm_length"]) * mutation_factor))
        self.assertTrue(new_child["speed"] > (individual1["speed"] + individual2["speed"]) / 2 -
                        ((individual1["speed"] + individual2["speed"]) * mutation_factor))
        self.assertTrue(new_child["speed"] < (individual1["speed"] + individual2["speed"]) / 2 +
                        ((individual1["speed"] + individual2["speed"]) * mutation_factor))
        self.assertTrue(new_child["strength"] > (individual1["strength"] + individual2["strength"]) / 2 -
                        ((individual1["strength"] + individual2["strength"]) * mutation_factor))
        self.assertTrue(new_child["strength"] < (individual1["strength"] + individual2["strength"]) / 2 +
                        ((individual1["strength"] + individual2["strength"]) * mutation_factor))
        self.assertTrue(new_child["jump"] > (individual1["jump"] + individual2["jump"]) / 2 -
                        ((individual1["jump"] + individual2["jump"]) * mutation_factor))
        self.assertTrue(new_child["jump"] < (individual1["jump"] + individual2["jump"]) / 2 +
                        ((individual1["jump"] + individual2["jump"]) * mutation_factor))
        self.assertTrue(
            new_child["skin_thickness"] > (individual1["skin_thickness"] + individual2["skin_thickness"]) / 2 -
            ((individual1["skin_thickness"] + individual2["skin_thickness"]) * mutation_factor))
        self.assertTrue(
            new_child["skin_thickness"] < (individual1["skin_thickness"] + individual2["skin_thickness"]) / 2 +
            ((individual1["skin_thickness"] + individual2["skin_thickness"]) * mutation_factor))
        return 1
