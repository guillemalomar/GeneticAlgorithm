import numpy as np
import random

from settings import mutation_factor
from src.model import Individual
from settings import initial_population_size, INDIVIDUALS_PARAMS


def reproduction_stage(iteration, current_population):
    individuals = []
    for i in range(0, initial_population_size - 2000):
        individuals.append(i)
    random.shuffle(individuals)
    old_individuals = []
    new_individuals = []
    for i in range(0, 4000):
        try:
            rand_ind1 = individuals.pop()
            ind1 = current_population[rand_ind1]
            ind1.set_id(i)
            rand_ind2 = individuals.pop()
            ind2 = current_population[rand_ind2]
            ind2.set_id(i+4000)
        except Exception as exc:
            print(exc)
        old_individuals.append(ind1)
        old_individuals.append(ind2)
        new_individuals.append(obtain_children(i + 8000, iteration, ind1,  ind2))
    old_individuals.extend(new_individuals)
    return old_individuals


def obtain_children(index, iteration, individual1, individual2):
    child = Individual()
    child.index = index
    child.age = int(index / 2000) + iteration
    child.height = np.clip((individual1.height + individual2.height) / 2 *
                           round(random.uniform(1 - mutation_factor, 1 + mutation_factor), 3),
                           INDIVIDUALS_PARAMS['height'][0] * 0.8,
                           INDIVIDUALS_PARAMS['height'][1] * 1.2)
    child.speed = np.clip((individual1.speed + individual2.speed) / 2 *
                          round(random.uniform(1 - mutation_factor, 1 + mutation_factor), 3),
                          INDIVIDUALS_PARAMS['speed'][0] * 0.8,
                          INDIVIDUALS_PARAMS['speed'][1] * 1.2)
    child.jump = np.clip((individual1.jump + individual2.jump) / 2 *
                         round(random.uniform(1 - mutation_factor, 1 + mutation_factor), 3),
                         INDIVIDUALS_PARAMS['jump'][0] * 0.8,
                         INDIVIDUALS_PARAMS['jump'][1] * 1.2)
    child.strength = np.clip((individual1.strength + individual2.strength) / 2 *
                             round(random.uniform(1 - mutation_factor, 1 + mutation_factor), 3),
                             INDIVIDUALS_PARAMS['strength'][0] * 0.8,
                             INDIVIDUALS_PARAMS['strength'][1] * 1.2)
    child.arm_length = np.clip((individual1.arm_length + individual2.arm_length) / 2 *
                               round(random.uniform(1 - mutation_factor, 1 + mutation_factor), 3),
                               INDIVIDUALS_PARAMS['arm_length'][0] * 0.8,
                               INDIVIDUALS_PARAMS['arm_length'][1] * 1.2)
    child.skin_thickness = np.clip((individual1.skin_thickness + individual2.skin_thickness) / 2 *
                                   round(random.uniform(1 - mutation_factor, 1 + mutation_factor), 3),
                                   INDIVIDUALS_PARAMS['skin_thickness'][0] * 0.8,
                                   INDIVIDUALS_PARAMS['skin_thickness'][1] * 1.2)
    return child
