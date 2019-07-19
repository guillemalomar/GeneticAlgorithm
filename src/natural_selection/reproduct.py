import asyncio
import logging
import numpy as np
import random

from settings.settings import mutation_factor
from settings.settings import initial_population_size, INDIVIDUALS_PARAMS


def reproduction_stage(iteration, current_population):
    individuals = []
    for i in range(0, initial_population_size - int(initial_population_size / 2.5)):
        individuals.append(i)
    random.shuffle(individuals)
    old_individuals = []
    list_of_pairs = []
    for i in range(0, int(initial_population_size * 0.3)):
        ind1 = current_population[individuals.pop()]
        ind1['id'] = i
        old_individuals.append(ind1)
        ind2 = current_population[individuals.pop()]
        ind2['id'] = i + int(initial_population_size * 0.3)
        old_individuals.append(ind2)
        list_of_pairs.append((ind1, ind2))
    new_individuals = asyncio.run(pair_individuals(list_of_pairs, iteration))
    logging.debug("Created {} new individuals".format(len(new_individuals)))
    old_individuals.extend(new_individuals)
    return old_individuals


async def pair_individuals(list_of_pairs, iteration):
    tasks = []
    for ind, pair in enumerate(list_of_pairs):
        tasks.append(
            asyncio.ensure_future(
                obtain_children(ind + int(initial_population_size * 0.6),
                                iteration,
                                pair[0],
                                pair[1]
                                )
            )
        )
        tasks.append(
            asyncio.ensure_future(
                obtain_children(ind + int(initial_population_size * 0.6) + int(initial_population_size * 0.3),
                                iteration,
                                pair[0],
                                pair[1]
                                )
            )
        )
    responses = await asyncio.gather(*tasks)
    return responses


async def obtain_children(index, iteration, individual1, individual2):
    child = dict()
    child['index'] = index
    child['age'] = int(index / (initial_population_size / 5)) + iteration
    child['height'] = round(float(np.clip((individual1['height'] + individual2['height']) / 2 *
                                          random.uniform(1 - mutation_factor, 1 + mutation_factor),
                                          INDIVIDUALS_PARAMS['height'][0] * 0.8,
                                          INDIVIDUALS_PARAMS['height'][1] * 1.2)), 3)
    child['speed'] = round(float(np.clip((individual1['speed'] + individual2['speed']) / 2 *
                                         random.uniform(1 - mutation_factor, 1 + mutation_factor),
                                         INDIVIDUALS_PARAMS['speed'][0] * 0.8,
                                         INDIVIDUALS_PARAMS['speed'][1] * 1.2)), 3)
    child['jump'] = round(float(np.clip((individual1['jump'] + individual2['jump']) / 2 *
                                        random.uniform(1 - mutation_factor, 1 + mutation_factor),
                                        INDIVIDUALS_PARAMS['jump'][0] * 0.8,
                                        INDIVIDUALS_PARAMS['jump'][1] * 1.2)), 3)
    child['strength'] = round(float(np.clip((individual1['strength'] + individual2['strength']) / 2 *
                                            random.uniform(1 - mutation_factor, 1 + mutation_factor),
                                            INDIVIDUALS_PARAMS['strength'][0] * 0.8,
                                            INDIVIDUALS_PARAMS['strength'][1] * 1.2)), 3)
    child['arm_length'] = round(float(np.clip((individual1['arm_length'] + individual2['arm_length']) / 2 *
                                              random.uniform(1 - mutation_factor, 1 + mutation_factor),
                                              INDIVIDUALS_PARAMS['arm_length'][0] * 0.8,
                                              INDIVIDUALS_PARAMS['arm_length'][1] * 1.2)), 3)
    child['skin_thickness'] = round(float(np.clip((individual1['skin_thickness'] + individual2['skin_thickness']) / 2 *
                                                  random.uniform(1 - mutation_factor, 1 + mutation_factor),
                                                  INDIVIDUALS_PARAMS['skin_thickness'][0] * 0.8,
                                                  INDIVIDUALS_PARAMS['skin_thickness'][1] * 1.2)), 3)
    child['total_reach'] = round(child['height'] + child['jump'] + child['arm_length'], 3)
    return child
