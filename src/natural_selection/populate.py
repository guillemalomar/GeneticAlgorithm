import logging
import random

from src.tools import check_db, return_db
from src import is_generic, get_population_size
from settings.generic_model import GENERIC_PARAMS
from settings.human_model import HUMAN_PARAMS


def create_individuals(environment_name):
    """
    This method creates the initial set of individuals that will be tested against the environment
    :param environment_name: name of the environment
    :type environment_name: str
    :return: resulting set of individuals
    :rtype: list or DBWrapper
    """
    current_population = []
    if check_db():
        return_db().create_collection_and_set('{}_{}'.format(environment_name, 1))
        current_population = return_db()
    for index in range(0, get_population_size()):
        params = obtain_params(index)
        if check_db():
            return_db().insert_document('{}_{}'.format(environment_name, 1), params)
        else:
            current_population.append(params)
    logging.debug("Created a starting set of {} individuals".format(get_population_size()))
    return current_population


def obtain_params(index):
    """
    This method creates an individual for the first iteration, by randomly obtaining values in a defined range for
    each parameters, and assigning an age and initial iteration
    :param index: individual index
    :type index: int
    :return: the individual containing all its parameters
    :rtype: dict
    """
    params = {
        '_id': index,
        'age': int(index / (get_population_size() / 5)) + 1
    }
    if not is_generic():
        for k, v in HUMAN_PARAMS.items():
            params[k] = round(random.uniform(v[0], v[1]), 3)
        params['total_reach'] = round(params['height'] + params['jump'] + params['arm_length'], 3)
    else:
        for k, v in GENERIC_PARAMS.items():
            params[k] = round(random.uniform(v[0], v[1]), 3)
    return params
