import random

from src.tools import my_mongo_wrapper
from settings import INDIVIDUALS_PARAMS, initial_population_size


def create_individuals(environment_name):
    current_population = []
    my_mongo_wrapper.create_collection(environment_name, 1)
    for index in range(0, initial_population_size):
        params = obtain_params(index)
        my_mongo_wrapper.insert_document_into_collection(environment_name, 1, params)
    return current_population


def obtain_params(index):
    params = {
        'id': index,
        'age': int(index / 2000) + 1,
        'iteration': 1
    }
    for k, v in INDIVIDUALS_PARAMS.items():
        params[k] = round(random.uniform(v[0], v[1]), 3)
    params['total_reach'] = round(params['height'] + params['jump'] + params['arm_length'], 3)
    return params
