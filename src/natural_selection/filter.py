import asyncio
import logging

from settings.settings import initial_population_size


def filter_individuals(current_population, environment):
    """

    :param current_population:
    :type current_population: list of individuals
    :return:
    :rtype: list of individuals
    """
    valued_individuals = asyncio.run(create_evaluation_tasks(current_population, environment))
    valued_individuals = [y[0] for y in sorted(valued_individuals, key=lambda x: x[1])]
    valued_individuals = valued_individuals[int(initial_population_size * 0.4):]
    logging.debug("Deleted {} individuals".format(int(initial_population_size * 0.4)))
    return valued_individuals


async def create_evaluation_tasks(current_population, environment):
    tasks = [asyncio.ensure_future(evaluate_individual(individual, environment)) for individual in current_population]
    responses = await asyncio.gather(*tasks)
    return responses


async def evaluate_individual(individual, environment):
    """
    This method obtains an overall value for an individual in an environment
    :param individual:
    :type individual:
    :param environment:
    :type environment:
    :return:
    :rtype:
    """
    individual_value = value_function(individual, environment)
    individual_value = individual_value * 0.5 if not check_enough_food(individual, environment) else individual_value
    individual_value = check_too_good(individual, individual_value, environment)
    individual_value = check_fast_enough(individual, individual_value, environment)
    individual_value = check_warm_enough(individual, individual_value, environment)
    return individual, individual_value


def value_function(individual, environment):
    """
    This method checks how good are the individual parameters
    :param individual:
    :type individual:
    :param environment:
    :type environment:
    :return:
    :rtype:
    """
    temp_threshold = 0.05 + (abs(environment['temperature'] - 20) * (0.30 / 30))
    total_value = 0
    total_reach = individual['height'] + individual['arm_length'] + individual['jump']
    total_value += 4 * total_reach / environment['tree_height']
    total_value += individual['strength'] / environment['food_animals_strength']
    total_value += individual['speed'] / environment['predators_speed']
    total_value += individual['skin_thickness'] / temp_threshold
    return total_value


def check_enough_food(individual, environment):
    """
    This method checks if the individual will be able to obtain food in some way.
    :param individual:
    :type individual: Individual
    :return:
    :rtype: float
    """
    if (individual['total_reach'] < environment['tree_height']) or \
        (individual['speed'] < environment['food_animals_speed'] and
         individual['strength'] < environment['food_animals_strength']):
        return False
    return True


def check_tall_enough(individual, environment):
    total_reach = individual['height'] + individual['arm_length'] + individual['jump']
    if total_reach < environment['tree_height']:
        return False
    return True


def check_too_good(individual, total_value, environment):
    """
    This method checks if the individual has some parameter that is too good, and lowers it down (as it's not 'economic'
    to have an overpowered parameter)
    :param individual:
    :type individual: Individual
    :param total_value:
    :type total_value: float
    :return:
    :rtype: float
    """
    ind_speed_vs_predator = individual['speed'] / environment['predators_speed']
    ind_speed_vs_food = individual['speed'] / environment['food_animals_speed']
    ind_strength_vs_food = individual['strength'] / environment['food_animals_strength']
    temp_threshold = 0.05 + (abs(environment['temperature'] - 20) * (0.30 / 30))

    if individual['total_reach'] / environment['tree_height'] > 1.1:
        total_value = total_value * 0.7

    if individual['skin_thickness'] / temp_threshold > 1.1:
        total_value = total_value * 0.7

    if ind_strength_vs_food > 1.1:
        total_value = total_value * 0.7

    if ind_speed_vs_food > 1.1 and \
       is_fast_enough(individual, environment):
        total_value = total_value * 0.7

    if ind_speed_vs_predator > 1.1:
        total_value = total_value * 0.7

    return total_value


def is_fast_enough(individual, environment):
    """

    :param individual:
    :type individual:
    :param environment:
    :type environment:
    :return:
    :rtype:
    """
    if individual['speed'] < environment['predators_speed']:
        return False
    return True


def check_strong_enough(individual, environment):
    if individual['strength'] < environment['food_animals_strength']:
        return False
    return True


def check_fast_enough(individual, total_value, environment):
    """
    Check if the individual's speed is high enough to scape from predators. Otherwise give a big penalization.
    :param individual:
    :type individual: Individual
    :param total_value:
    :type total_value: float
    :return:
    :rtype: float
    """
    if not is_fast_enough(individual, environment):
        total_value = total_value * 0.1
    else:
        total_value = total_value * 2
    return total_value


def is_warm_enough(individual, environment):
    """

    :param individual:
    :type individual:
    :param environment:
    :type environment:
    :return:
    :rtype:
    """
    temp_threshold = 0.05 + (abs(environment['temperature'] - 20) * (0.30 / 30))
    if individual['skin_thickness'] < temp_threshold:
        return False
    return True


def check_warm_enough(individual, total_value, environment):
    """
    Check if the individual's speed is high enough to scape from predators. Otherwise give a big penalization.
    :param individual:
    :type individual: Individual
    :param total_value:
    :type total_value: float
    :return:
    :rtype: float
    """
    if not is_warm_enough(individual, environment):
        total_value = total_value * 0.1
    else:
        total_value = total_value * 1.5
    return total_value


def natural_death(iteration, current_population):
    """
    Kill all individuals which have as age the current iteration
    :return:
    :rtype: list of Individual
    """
    young_individuals = []
    for individual in current_population:
        if individual['age'] > iteration:
            young_individuals.append(individual)
    young_individuals = young_individuals[0: initial_population_size]
    logging.debug("{} individuals died of natural causes".format(int(len(current_population) - len(young_individuals))))
    return young_individuals
