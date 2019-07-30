import asyncio
import logging
import numpy as np
import random

from settings.settings import mutation_factor, initial_population_size, INDIVIDUALS_PARAMS


def reproduction_stage(iteration, current_population):
    """
    This method pairs random individuals, obtains their children, and adds them to the population
    :param iteration: current iteration
    :type iteration: int
    :param current_population: set of individuals to reproduce
    :type current_population: list or MongoWrapper
    :return: resulting set of individuals after reproduction stage
    :rtype: list or DBWrapper
    """
    random_individuals_pairs = obtain_randomized_pairs(int(initial_population_size * 0.6))
    if type(current_population) is list:
        new_iter_individuals = obtain_randomized_pairs_of_individuals(
            current_population,
            random_individuals_pairs
        )
        newly_created_individuals = asyncio.run(pair_individuals(current_population,
                                                                 random_individuals_pairs,
                                                                 iteration))
        logging.debug("Created {} new individuals".format(len(newly_created_individuals)))
        new_iter_individuals.extend(newly_created_individuals)
        return new_iter_individuals
    else:
        filtered_population = current_population.current_collection
        reproduction_coll = '{}_{}'.format('_'.join(filtered_population.name.split('_')[0:-1]), 'reproduced')
        current_population.create_collection_and_set(reproduction_coll)
        list_of_pairs = mongo_obtain_randomized_pairs_of_individuals(
                current_population,
                filtered_population,
                random_individuals_pairs
        )
        newly_created_individuals = asyncio.run(pair_individuals(current_population,
                                                                 list_of_pairs,
                                                                 iteration))
        logging.debug("Created {} new individuals".format(len(newly_created_individuals)))
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
    for i in range(0, int(initial_population_size * 0.3)):
        ind1 = random_individuals.pop()
        ind2 = random_individuals.pop()
        random_pairs.append((ind1, ind2))
    return random_pairs


def mongo_obtain_randomized_pairs_of_individuals(current_population, filtered_population, random_individuals_pairs):
    """
    This method inserts the reproduction stage 'parents' into the new collection
    :param current_population: individuals to reproduce
    :type current_population: DBWrapper instance
    :param filtered_population: the specific population to be reproduced
    :type filtered_population: MongoCollectionWrapper instance
    :param random_individuals_pairs: list of randomized pairs
    :type random_individuals_pairs: list of tuples of 2 ints
    :return: list of randomized pairs
    :rtype: list of tuples of 2 ints
    """
    new_iter_individuals = []
    for index, random_individual_pair in enumerate(random_individuals_pairs):
        ind1 = filtered_population[random_individual_pair[0]]
        ind1['_id'] = index
        current_population.current_collection.insert_one(ind1)
        new_iter_individuals.append(ind1)
        ind2 = filtered_population[random_individual_pair[1]]
        ind2['_id'] = index + int(initial_population_size * 0.3)
        current_population.current_collection.insert_one(ind2)
    return random_individuals_pairs


def obtain_randomized_pairs_of_individuals(current_population, random_individuals_pairs):
    """
    This method inserts the reproduction stage 'parents' into the new collection
    :param current_population: individuals to reproduce
    :type current_population: list
    :param random_individuals_pairs: list of randomized pairs
    :type random_individuals_pairs: list of tuples of 2 ints
    :return: parents added to a new list
    :rtype: list of dicts
    """
    new_iter_individuals = []
    for index, random_individual_pair in enumerate(random_individuals_pairs):
        ind1 = current_population[random_individual_pair[0]]
        ind1['_id'] = index
        new_iter_individuals.append(ind1)
        ind2 = current_population[random_individual_pair[1]]
        ind2['_id'] = index + int(initial_population_size * 0.3)
        new_iter_individuals.append(ind2)
    return new_iter_individuals


async def pair_individuals(current_population, list_of_pairs, iteration):
    """
    This method creates the asynchronous tasks to obtain two childs for each pair of parents
    :param current_population: individuals to reproduce
    :type current_population: list or DBWrapper
    :param list_of_pairs: list of randomized pairs
    :type list_of_pairs: list of tuples of 2 ints
    :param iteration: current iteration
    :type iteration: int
    :return: list of the obtained children or list of _id's of the new children
    :rtype: list of dicts or list of ints
    """
    tasks = []
    for ind, pair in enumerate(list_of_pairs):
        tasks.append(
            asyncio.ensure_future(
                obtain_children(ind + int(initial_population_size * 0.6),
                                iteration,
                                pair[0],
                                pair[1],
                                current_population
                                )
            )
        )
        tasks.append(
            asyncio.ensure_future(
                obtain_children(ind + int(initial_population_size * 0.6) + int(initial_population_size * 0.3),
                                iteration,
                                pair[0],
                                pair[1],
                                current_population
                                )
            )
        )
    responses = await asyncio.gather(*tasks)
    return responses


async def obtain_children(index, iteration, individual1_ind, individual2_ind, current_population):
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
    :return: obtained child or _id of the new child
    :rtype: dict or int
    """
    if type(current_population) is list:
        individual1 = current_population[individual1_ind]
        individual2 = current_population[individual2_ind]
    else:
        individual1 = current_population.current_collection[individual1_ind]
        individual2 = current_population.current_collection[individual2_ind]
    child = dict()
    child['_id'] = index
    child['age'] = int(index / (initial_population_size / 5)) + iteration
    child['height'] = round(
        float(np.clip((individual1['height'] + individual2['height']) / 2 * random.uniform(1 - mutation_factor,
                                                                                           1 + mutation_factor),
                      INDIVIDUALS_PARAMS['height'][0] * 0.8,
                      INDIVIDUALS_PARAMS['height'][1] * 1.2)),
        3
    )
    child['speed'] = round(
        float(np.clip((individual1['speed'] + individual2['speed']) / 2 * random.uniform(1 - mutation_factor,
                                                                                         1 + mutation_factor),
                      INDIVIDUALS_PARAMS['speed'][0] * 0.8,
                      INDIVIDUALS_PARAMS['speed'][1] * 1.2)),
        3
    )
    child['jump'] = round(
        float(np.clip((individual1['jump'] + individual2['jump']) / 2 * random.uniform(1 - mutation_factor,
                                                                                       1 + mutation_factor),
                      INDIVIDUALS_PARAMS['jump'][0] * 0.8,
                      INDIVIDUALS_PARAMS['jump'][1] * 1.2)),
        3
    )
    child['strength'] = round(
        float(np.clip((individual1['strength'] + individual2['strength']) / 2 * random.uniform(1 - mutation_factor,
                                                                                               1 + mutation_factor),
                      INDIVIDUALS_PARAMS['strength'][0] * 0.8,
                      INDIVIDUALS_PARAMS['strength'][1] * 1.2)),
        3
    )
    child['arm_length'] = round(
        float(np.clip((individual1['arm_length'] + individual2['arm_length']) / 2 * random.uniform(1 - mutation_factor,
                                                                                                   1 + mutation_factor),
                      INDIVIDUALS_PARAMS['arm_length'][0] * 0.8,
                      INDIVIDUALS_PARAMS['arm_length'][1] * 1.2)),
        3
    )
    child['skin_thickness'] = round(
        float(np.clip(
            (individual1['skin_thickness'] + individual2['skin_thickness']) / 2 * random.uniform(1 - mutation_factor,
                                                                                                 1 + mutation_factor),
            INDIVIDUALS_PARAMS['skin_thickness'][0] * 0.8,
            INDIVIDUALS_PARAMS['skin_thickness'][1] * 1.2)),
        3
    )
    child['total_reach'] = round(child['height'] + child['jump'] + child['arm_length'], 3)
    if type(current_population) is not list:
        current_population.current_collection.insert_one(child)
        return index
    return child
