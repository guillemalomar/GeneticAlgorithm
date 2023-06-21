import asyncio
import logging
import numpy as np
import random

from settings.human_model import HUMAN_PARAMS
from settings.generic_model import GENERIC_PARAMS
from src import is_generic, is_elitist, get_mutation_factor, get_population_size


def reproduction_stage(iteration, current_population, environment_name):
    """
    This method pairs random individuals, obtains their children, and adds them to the population
    :param iteration: current iteration
    :type iteration: int
    :param current_population: set of individuals to reproduce
    :type current_population: list or MongoWrapper
    :param environment_name:
    :type environment_name:
    :return: resulting set of individuals after reproduction stage
    :rtype: list or DBWrapper
    """
    filtered_coll = f"{environment_name}_{iteration}_filtered"
    reproduce_coll = f"{environment_name}_{iteration}_reproduction"
    individuals_pairs = obtain_randomized_pairs(int(get_population_size() * 0.6)) if is_elitist() \
        else obtain_ordered_pairs(int(get_population_size() * 0.6))
    new_iter_individuals = obtain_pairs_of_individuals(
        current_population,
        individuals_pairs,
        filtered_coll,
    )
    newly_created_individuals = asyncio.run(pair_individuals(current_population,
                                                             individuals_pairs,
                                                             iteration,
                                                             filtered_coll))
    logging.debug(f"Created {len(newly_created_individuals)} new individuals")
    current_population[reproduce_coll].extend(new_iter_individuals)
    return current_population


def obtain_randomized_pairs(current_population_len):
    """
    This method obtains a randomized pairs list containing all current individuals
    :param current_population_len: total number of individuals to randomize
    :type current_population_len: int
    :return: the resulting list of randomized pairs
    :rtype: list of tuples of 2 ints
    """
    random_individuals = [i for i in range(0, current_population_len)]
    random.shuffle(random_individuals)
    random_pairs = []
    for i in range(0, int(get_population_size() * 0.3)):
        ind1 = random_individuals.pop()
        ind2 = random_individuals.pop()
        random_pairs.append((ind1, ind2))
    return random_pairs


def obtain_ordered_pairs(current_population_len):
    """
    This method obtains an ordered pairs list containing all current individuals
    :param current_population_len: total number of individuals to randomize
    :type current_population_len: int
    :return: the resulting list of ordered pairs
    :rtype: list of tuples of 2 ints
    """
    ordered_pairs = []
    for i in range(0, current_population_len, 2):
        ordered_pairs.append((i, i + 1))
    return ordered_pairs


def mongo_obtain_pairs_of_individuals(current_population, filtered_population, individuals_pairs):
    """
    This method inserts the reproduction stage 'parents' into the new collection
    :param current_population: individuals to reproduce
    :type current_population: DBWrapper instance
    :param filtered_population: the specific population to be reproduced
    :type filtered_population: MongoCollectionWrapper instance
    :param individuals_pairs: list of pairs
    :type individuals_pairs: list of tuples of 2 ints
    :return: list of randomized pairs
    :rtype: list of tuples of 2 ints
    """
    for index, individual_pair in enumerate(individuals_pairs):
        for index2, step in enumerate([0, int(get_population_size() * 0.3)]):
            individual = filtered_population[individual_pair[index2]]
            individual["_id"] = index
            current_population.current_collection.insert_one(individual)
    return individuals_pairs


def obtain_pairs_of_individuals(current_population, individuals_pairs, filtered_coll):
    """
    This method inserts the reproduction stage 'parents' into the new collection
    :param current_population: individuals to reproduce
    :type current_population: list
    :param individuals_pairs: list of pairs
    :type individuals_pairs: list of tuples of 2 ints
    :param filtered_coll: name of the filtered collection
    :type filtered_coll: str
    :return: parents added to a new list
    :rtype: list of dicts
    """
    new_iter_individuals = []
    for index, individual_pair in enumerate(individuals_pairs):
        ind1 = current_population[filtered_coll][individual_pair[0]]
        ind1["_id"] = index
        new_iter_individuals.append(ind1)
        ind2 = current_population[filtered_coll][individual_pair[1]]
        ind2["_id"] = index + int(get_population_size() * 0.3)
        new_iter_individuals.append(ind2)
    return new_iter_individuals


async def pair_individuals(current_population, list_of_pairs, iteration, filtered_coll):
    """
    This method creates the asynchronous tasks to obtain two children for each pair of parents
    :param current_population: individuals to reproduce
    :type current_population: list or DBWrapper
    :param list_of_pairs: list of randomized pairs
    :type list_of_pairs: list of tuples of 2 ints
    :param iteration: current iteration
    :type iteration: int
    :param filtered_coll: name of the filtered collection
    :type filtered_coll: str
    :return: list of the obtained children or list of _id's of the new children
    :rtype: list of dicts or list of ints
    """
    tasks = []
    for ind, pair in enumerate(list_of_pairs):
        for step in [0, int(get_population_size() * 0.3)]:
            tasks.append(
                asyncio.ensure_future(
                    obtain_children(ind + int(get_population_size() * 0.6) + step,
                                    iteration,
                                    pair[0],
                                    pair[1],
                                    current_population,
                                    filtered_coll,
                                    )
                )
            )
    responses = await asyncio.gather(*tasks)
    return responses


async def obtain_children(index, iteration, individual1_ind, individual2_ind, current_population, filtered_coll):
    """
    This method takes the indexes of the new child parents, obtains the parents parameters, and creates the
    new child parameters from the average of each of the parents parameters, adding a small mutation factor
    :param index: _id of the new children
    :type index: int
    :param iteration: current iteration
    :type iteration: int
    :param individual1_ind: parent 1 _id
    :type individual1_ind: int
    :param individual2_ind: parent 1 _id
    :type individual2_ind: int
    :param current_population: individuals to reproduce
    :type current_population: list or DBWrapper
    :param filtered_coll: name of the filtered collection
    :type filtered_coll: str
    :return: obtained child or _id of the new child
    :rtype: dict or int
    """
    ind1 = current_population[filtered_coll][individual1_ind]
    ind2 = current_population[filtered_coll][individual2_ind]
    child = {
        "value": 0,
        "_id": index,
        "age": int((index - int(get_population_size() * 0.6)) / int(get_population_size() * 0.6 / 5)) + iteration + 1
    }
    mutation_factor = get_mutation_factor()
    params_to_read = GENERIC_PARAMS if is_generic() else HUMAN_PARAMS
    for parameter, value in ind1.items():
        if parameter not in ["_id", "age", "value"]:
            child[parameter] = round(
                float(np.clip(
                    (ind1[parameter] + ind2[parameter]) / 2 * random.uniform(1 - mutation_factor,
                                                                             1 + mutation_factor),
                    params_to_read[parameter][0] * 0.8,
                    params_to_read[parameter][1] * 1.2)),
                3
            )
    reproduction_collection = f"{'_'.join(filtered_coll.split('_')[:-1])}_reproduction"
    current_population[reproduction_collection].append(child)
    return index
