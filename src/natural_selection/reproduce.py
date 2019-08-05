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
    filtered_coll = '{}_{}_filtered'.format(environment_name, iteration)
    reproduce_coll = '{}_{}_reproduction'.format(environment_name, iteration)
    if is_elitist():
        individuals_pairs = obtain_randomized_pairs(int(get_population_size() * 0.6))
    else:
        individuals_pairs = obtain_ordered_pairs(int(get_population_size() * 0.6))
    new_iter_individuals = obtain_pairs_of_individuals(
        current_population,
        individuals_pairs,
        filtered_coll
    )
    newly_created_individuals = asyncio.run(pair_individuals(current_population,
                                                             individuals_pairs,
                                                             iteration,
                                                             filtered_coll))
    logging.debug("Created {} new individuals".format(len(newly_created_individuals)))
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
    new_iter_individuals = []
    for index, individual_pair in enumerate(individuals_pairs):
        ind1 = filtered_population[individual_pair[0]]
        ind1['_id'] = index
        current_population.current_collection.insert_one(ind1)
        new_iter_individuals.append(ind1)
        ind2 = filtered_population[individual_pair[1]]
        ind2['_id'] = index + int(get_population_size() * 0.3)
        current_population.current_collection.insert_one(ind2)
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
        ind1['_id'] = index
        new_iter_individuals.append(ind1)
        ind2 = current_population[filtered_coll][individual_pair[1]]
        ind2['_id'] = index + int(get_population_size() * 0.3)
        new_iter_individuals.append(ind2)
    return new_iter_individuals


async def pair_individuals(current_population, list_of_pairs, iteration, filtered_coll):
    """
    This method creates the asynchronous tasks to obtain two childs for each pair of parents
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
        tasks.append(
            asyncio.ensure_future(
                obtain_children(ind + int(get_population_size() * 0.6),
                                iteration,
                                pair[0],
                                pair[1],
                                current_population,
                                filtered_coll
                                )
            )
        )
        tasks.append(
            asyncio.ensure_future(
                obtain_children(ind + int(get_population_size() * 0.6) + int(get_population_size() * 0.3),
                                iteration,
                                pair[0],
                                pair[1],
                                current_population,
                                filtered_coll
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
    child = dict()
    child['_id'] = index
    child['age'] = int((index - int(get_population_size()*0.6)) / int(get_population_size()*0.6 / 5)) \
        + iteration \
        + 1
    mutation_factor = get_mutation_factor()
    if not is_generic():
        child['height'] = round(
            float(np.clip((ind1['height'] + ind2['height']) / 2 * random.uniform(1 - mutation_factor,
                                                                                 1 + mutation_factor),
                          HUMAN_PARAMS['height'][0] * 0.8,
                          HUMAN_PARAMS['height'][1] * 1.2)),
            3
        )
        child['speed'] = round(
            float(np.clip((ind1['speed'] + ind2['speed']) / 2 * random.uniform(1 - mutation_factor,
                                                                               1 + mutation_factor),
                          HUMAN_PARAMS['speed'][0] * 0.8,
                          HUMAN_PARAMS['speed'][1] * 1.2)),
            3
        )
        child['jump'] = round(
            float(np.clip((ind1['jump'] + ind2['jump']) / 2 * random.uniform(1 - mutation_factor,
                                                                             1 + mutation_factor),
                          HUMAN_PARAMS['jump'][0] * 0.8,
                          HUMAN_PARAMS['jump'][1] * 1.2)),
            3
        )
        child['strength'] = round(
            float(np.clip((ind1['strength'] + ind2['strength']) / 2 * random.uniform(1 - mutation_factor,
                                                                                     1 + mutation_factor),
                          HUMAN_PARAMS['strength'][0] * 0.8,
                          HUMAN_PARAMS['strength'][1] * 1.2)),
            3
        )
        child['arm_length'] = round(
            float(np.clip((ind1['arm_length'] + ind2['arm_length']) / 2 * random.uniform(1 - mutation_factor,
                                                                                         1 + mutation_factor),
                          HUMAN_PARAMS['arm_length'][0] * 0.8,
                          HUMAN_PARAMS['arm_length'][1] * 1.2)),
            3
        )
        child['skin_thickness'] = round(
            float(np.clip(
                (ind1['skin_thickness'] + ind2['skin_thickness']) / 2 * random.uniform(1 - mutation_factor,
                                                                                       1 + mutation_factor),
                HUMAN_PARAMS['skin_thickness'][0] * 0.8,
                HUMAN_PARAMS['skin_thickness'][1] * 1.2)),
            3
        )
    else:
        for param, value in ind1.items():
            if param != '_id' and param != 'age' and param != 'value':
                child[param] = round(
                    float(np.clip(
                        (ind1[param] + ind2[param]) / 2 * random.uniform(1 - mutation_factor,
                                                                         1 + mutation_factor),
                        GENERIC_PARAMS[param][0] * 0.8,
                        GENERIC_PARAMS[param][1] * 1.2)),
                    3
                )
    child['value'] = 0
    reproduction_collection = '{}_{}'.format('_'.join(filtered_coll.split('_')[:-1]), 'reproduction')
    current_population[reproduction_collection].append(child)
    return index
