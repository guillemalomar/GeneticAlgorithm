import random

from src import CURRENT_POPULATION
from src.model import Individual
# from src.tools import my_sql_wrapper
from settings import INDIVIDUALS_PARAMS, initial_population_size


def create_individuals():
    for index in range(0, initial_population_size):
        params = obtain_params(index)
        my_ind = Individual()
        my_ind.create(identifier=index, **params)
        CURRENT_POPULATION.append(my_ind)
        # my_sql_wrapper.insert_individual(my_ind)


def obtain_params(index):
    params = {
        'age': int(index / 200) + 1,
        'iteration': 1
    }
    for k, v in INDIVIDUALS_PARAMS.items():
        params[k] = round(random.uniform(v[0], v[1]), 3)
    return params
