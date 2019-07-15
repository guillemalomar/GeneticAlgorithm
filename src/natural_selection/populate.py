import random

from src.model import Individual
from src.tools import my_sql_wrapper
from settings import INDIVIDUALS_PARAMS, initial_population


def create_individuals():
    for i in range(1, initial_population):
        params = obtain_params(i)
        my_ind = Individual()
        my_ind.create(**params)
        my_sql_wrapper.insert_individual(my_ind)


def obtain_params(individual_id):
    params = {
        'age': 1,
        'iteration': 1
    }
    for k, v in INDIVIDUALS_PARAMS.items():
        params[k] = round(random.uniform(v[0], v[1]), 3)
    return params
