import asyncio
import logging

from settings.settings import initial_population_size, PARAMETER_WEIGHTS


def filter_individuals(current_population, environment):
    """
    Main filter method
    :param current_population: set of individuals to test against the environment
    :type current_population: list or DBWrapper
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: resulting set of individuals after filtering stage
    :rtype: list or DBWrapper
    """
    if type(current_population) is list:
        valued_individuals = asyncio.run(create_evaluation_tasks(current_population, environment))
        valued_individuals = [y[0] for y in sorted(valued_individuals, key=lambda x: x[1], reverse=True)]
        valued_individuals = valued_individuals[:int(initial_population_size * 0.6)]
        logging.debug("Deleted {} individuals".format(int(initial_population_size * 0.4)))
        return valued_individuals
    else:
        coll = current_population.current_collection
        valued_individuals = asyncio.run(create_evaluation_tasks(coll, environment))
        for individual in valued_individuals:
            coll[individual[0]['_id']] = individual[0]
        current_population.create_collection_and_set('{}_{}'.format(coll.name, 'filtered'))
        for it_id, item in enumerate(coll.find({},
                                               sort=("value", -1),
                                               limit=int(initial_population_size * 0.6))):
            current_population.current_collection[it_id] = item
        return current_population


async def create_evaluation_tasks(current_population, environment):
    """
    Creates a task for each individual and waits for the result
    :param current_population: set of individuals to test against the environment
    :type current_population: list or DBWrapper
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: pairs of individuals with their values
    :rtype: list of tuples of floats
    """
    tasks = [
        asyncio.ensure_future(evaluate_individual(current_population, individual_id, environment))
        for individual_id in range(0, initial_population_size)
    ]
    responses = await asyncio.gather(*tasks)
    return responses


async def evaluate_individual(current_population, individual_id, environment):
    """
    This method obtains an overall value for an individual in an environment
    :param current_population: set of individuals to test against the environment
    :type current_population: list or DBWrapper
    :param individual_id: id of the individual to evaluate
    :type individual_id: int
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: pair of individual with its value
    :rtype: tuple
    """
    individual = current_population[individual_id]
    individual_value = value_function(individual, environment)
    individual_value = individual_value * 0.5 if not is_food_accessible(individual, environment) else individual_value
    individual_value = check_too_good(individual, individual_value, environment)
    individual_value = evaluate_fast_enough(individual, individual_value, environment)
    individual_value = evaluate_warm_enough(individual, individual_value, environment)
    individual['value'] = individual_value
    return individual, individual_value


def value_function(individual, environment):
    """
    This method checks how good are the individual parameters
    :param individual: current individual parameters
    :type individual: dict
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: evaluation result
    :rtype: float
    """
    skin_threshold = 0.05 + (abs(environment['temperature'] - 20) * (0.30 / 30))
    total_reach = individual['height'] + individual['arm_length'] + individual['jump']

    total_value = 0
    total_value += PARAMETER_WEIGHTS['total_reach'] * min(total_reach / environment['tree_height'], 1)
    total_value += PARAMETER_WEIGHTS['strength'] * min(individual['strength'] / environment['food_animals_strength'], 1)
    total_value += PARAMETER_WEIGHTS['speed'] * min(individual['speed'] / environment['predators_speed'], 1)
    total_value += PARAMETER_WEIGHTS['skin_thickness'] * min(individual['skin_thickness'] / skin_threshold, 1)
    return total_value


def check_too_good(individual, total_value, environment):
    """
    This method checks if the individual has some parameter that is too good, and lowers it down (as it's not 'economic'
    to have an overpowered parameter)
    :param individual: current individual parameters
    :type individual: dict
    :param total_value: current evaluation for the individual
    :type total_value: float
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: new evaluation for the individual
    :rtype: float
    """
    skin_threshold = 0.05 + (abs(environment['temperature'] - 20) * (0.30 / 30))
    ind_speed_vs_predator = individual['speed'] / environment['predators_speed']
    ind_speed_vs_food = individual['speed'] / environment['food_animals_speed']
    ind_strength_vs_food = individual['strength'] / environment['food_animals_strength']
    ind_skin_vs_temp = individual['skin_thickness'] / skin_threshold
    ind_reach_vs_trees = individual['total_reach'] / environment['tree_height']

    if ind_reach_vs_trees > 1.1:
        total_value = total_value * 0.5

    if ind_skin_vs_temp > 1.1:
        total_value = total_value * 0.3

    if ind_strength_vs_food > 1.1:
        total_value = total_value * 0.5

    if ind_speed_vs_food > 1.1 and \
       ind_speed_vs_predator >= 1.0:
        total_value = total_value * 0.5

    if ind_speed_vs_predator > 1.1:
        total_value = total_value * 0.5

    return total_value


def evaluate_fast_enough(individual, total_value, environment):
    """
    Check if the individual's speed is high enough to scape from predators. Otherwise give a big penalization.
    :param individual: current individual parameters
    :type individual: dict
    :param total_value: current evaluation for the individual
    :type total_value: float
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: new evaluation for the individual
    :rtype: float
    """
    if not is_fast_enough(individual, environment):
        total_value = total_value * 0.2
    return total_value


def evaluate_warm_enough(individual, total_value, environment):
    """
    Check if the individual's skin is thick enough. Otherwise give a big penalization.
    :param individual: current individual parameters
    :type individual: dict
    :param total_value: current evaluation for the individual
    :type total_value: float
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: new evaluation for the individual
    :rtype: float
    """
    if not is_warm_enough(individual, environment):
        total_value = total_value * 0.2
    return total_value


def is_fast_enough(individual, environment):
    """
    This method checks if the individual can scape from predators
    :param individual: current individual parameters
    :type individual: dict
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: true if the individual is fast enough to scape from its predators. false otherwise.
    :rtype: bool
    """
    if individual['speed'] < environment['predators_speed']:
        return False
    return True


def is_strong_enough(individual, environment):
    """
    This method checks if the individual can kill for food
    :param individual: current individual parameters
    :type individual: dict
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: true if the individual is strong enough to kill food animals. false otherwise.
    :rtype: bool
    """
    if individual['strength'] <= environment['food_animals_strength']:
        return False
    return True


def is_warm_enough(individual, environment):
    """
    This method checks if the individual skin is thick enough to survive both low and high temperatures
    :param individual: current individual parameters
    :type individual: dict
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: true if the individual skin fits the environment temperature. false otherwise.
    :rtype: bool
    """
    temp_threshold = 0.05 + (abs(environment['temperature'] - 20) * (0.30 / 30))
    if individual['skin_thickness'] < temp_threshold:
        return False
    return True


def is_food_accessible(individual, environment):
    """
    This method checks if the individual will be able to obtain food in some way.
    :param individual: current individual parameters
    :type individual: dict
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: true if the individual has a way of finding food. false otherwise.
    :rtype: bool
    """
    if (individual['total_reach'] < environment['tree_height']) or \
        (individual['speed'] <= environment['food_animals_speed'] and
         individual['strength'] <= environment['food_animals_strength']):
        return False
    return True


def is_tall_enough(individual, environment):
    """
    This method checks if the individual can reach the food from the trees.
    :param individual: current individual parameters
    :type individual: dict
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: true if the individual can arrive to tree's food. false otherwise.
    :rtype: bool
    """
    total_reach = individual['height'] + individual['arm_length'] + individual['jump']
    if total_reach < environment['tree_height']:
        return False
    return True


def show_best_and_worst_fitting(current_population, iteration):
    """
    This method prints on terminal the best and worst valued individuals at a specific iteration
    :param current_population: set of individuals to test against the environment
    :type current_population: list or DBWrapper
    :param iteration: current iteration
    :type iteration: int
    """
    print("Iteration:  {}".format(iteration))
    if type(current_population) is not list:
        current_population = current_population.current_collection
    print("Worst individual: {}".format(current_population[int(initial_population_size * 0.6) - 1]))
    print("Best individual:  {}".format(current_population[0]))
