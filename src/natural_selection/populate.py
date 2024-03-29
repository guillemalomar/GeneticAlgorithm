import logging
import random

from src.tools import return_db
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
    current_population = return_db()
    for index in range(0, get_population_size()):
        individual_parameters = obtain_parameters(index)
        current_population[f"{environment_name}_1"].append(individual_parameters)
    logging.debug(f"Created a starting set of {get_population_size()} individuals")
    return current_population


def obtain_parameters(index):
    """
    This method creates an individual for the first iteration, by randomly obtaining values in a defined range for
    each parameters, and assigning an age and initial iteration
    :param index: individual index
    :type index: int
    :return: the individual containing all its parameters
    :rtype: dict
    """
    parameters = {
        "_id": index,
        "age": int(index / (get_population_size() / 5)) + 1,
        "value": 0
    }
    individual_parameters = dict(GENERIC_PARAMS) if is_generic() else dict(HUMAN_PARAMS)
    for k, v in individual_parameters.items():
        parameters[k] = round(random.uniform(v[0], v[1]), 3)
    return parameters
