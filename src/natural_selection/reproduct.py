import random

from settings import mutation_factor
from src.model import Individual
from settings import initial_population_size
from src import CURRENT_POPULATION


def reproduction_stage(iteration):
    individuals = []
    for i in range(0, initial_population_size):
        individuals.append(i)
    random.shuffle(individuals)
    new_individuals = []
    for i in range(0, 4000):
        ind1 = CURRENT_POPULATION[individuals.pop()]
        ind2 = CURRENT_POPULATION[individuals.pop()]
        new_individuals.append(obtain_children(i + 8000, iteration, ind1,  ind2))
    CURRENT_POPULATION.extend(new_individuals)


def obtain_children(index, iteration, individual1, individual2):
    child = Individual()
    child.index = index
    child.age = iteration
    child.height = (individual1.height + individual2.height) / 2 * \
        round(random.uniform(1 - mutation_factor, 1 + mutation_factor), 3)
    child.speed = (individual1.speed + individual2.speed) / 2 * \
        round(random.uniform(1 - mutation_factor, 1 + mutation_factor), 3)
    child.strength = (individual1.strength + individual2.strength) / 2 * \
        round(random.uniform(1 - mutation_factor, 1 + mutation_factor), 3)
    child.arm_length = (individual1.arm_length + individual2.arm_length) / 2 * \
        round(random.uniform(1 - mutation_factor, 1 + mutation_factor), 3)
    child.skin_thickness = (individual1.skin_thickness + individual2.skin_thickness) / 2 * \
        round(random.uniform(1 - mutation_factor, 1 + mutation_factor), 3)
    return child
