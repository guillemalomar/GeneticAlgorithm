import logging
import random

from src.tools import check_db, return_db
from settings.settings import INDIVIDUALS_PARAMS, initial_population_size


def create_individuals(environment_name):
    current_population = []
    if check_db():
        return_db().create_collection_and_set('{}_{}'.format(environment_name, 1))
        current_population = return_db()
    for index in range(0, initial_population_size):
        params = obtain_params(index)
        if check_db():
            return_db().insert_document('{}_{}'.format(environment_name, 1), params)
        else:
            current_population.append(params)
    logging.debug("Created a starting set of {} individuals".format(initial_population_size))
    return current_population


def obtain_params(index):
    params = {
        '_id': index,
        'age': int(index / 2000) + 1,
        'iteration': 1
    }
    for k, v in INDIVIDUALS_PARAMS.items():
        params[k] = round(random.uniform(v[0], v[1]), 3)
    params['total_reach'] = round(params['height'] + params['jump'] + params['arm_length'], 3)
    return params
