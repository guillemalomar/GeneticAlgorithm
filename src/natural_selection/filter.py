import asyncio
import logging
import operator

from settings.generic_model import GENERIC_WEIGHTS
from settings.human_model import HUMAN_WEIGHTS
from src import is_generic, get_population_size


def filter_individuals(current_population, environment, iteration):
    """
    Main filter method
    :param current_population: set of individuals to test against the environment
    :type current_population: list or DBWrapper
    :param environment: the current parameters against which the individuals are being tested
    :type environment: Environment
    :param iteration: current iteration
    :type iteration: int
    :return: resulting set of individuals after filtering stage
    :rtype: list or DBWrapper
    """
    filtered_collection = f"{environment.name}_{iteration}_filtered"
    _ = asyncio.run(create_evaluation_tasks(current_population, environment, iteration))
    current_population[filtered_collection].sort(key=operator.itemgetter("value"), reverse=True)
    deleted = 0
    for idx, item in enumerate(current_population[filtered_collection]):
        if idx < int(get_population_size() * 0.4):
            current_population[filtered_collection].pop(get_population_size() - idx - 1)
            deleted += 1
    logging.debug(f"Deleted {int(get_population_size() * 0.4)} individuals")
    return current_population


async def create_evaluation_tasks(current_population, environment, iteration):
    """
    Creates a task for each individual and waits for the result
    :param current_population: set of individuals to test against the environment
    :type current_population: list or DBWrapper
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :param iteration: current iteration
    :type iteration: int
    :return: pairs of individuals with their values
    :rtype: list of tuples of floats
    """
    tasks = [
        asyncio.ensure_future(evaluate_individual(current_population, individual_id, environment, iteration))
        for individual_id in range(0, get_population_size())
    ]
    responses = await asyncio.gather(*tasks)
    return responses


async def evaluate_individual(current_population, individual_id, environment, iteration):
    """
    This method obtains an overall value for an individual in an environment
    :param current_population: set of individuals to test against the environment
    :type current_population: list or DBWrapper
    :param individual_id: id of the individual to evaluate
    :type individual_id: int
    :param environment: the current parameters against which the individuals are being tested
    :type environment: Environment
    :param iteration: current iteration
    :type iteration: int
    :return: pair of individual with its value
    :rtype: tuple
    """
    base_coll_name = f"{environment.name}_{iteration}"
    individual = current_population[base_coll_name][individual_id]
    if not is_generic():
        individual_value = human_value_function(individual, environment.data)
        if not is_food_accessible(individual, environment.data):
            individual_value = individual_value * 0.5
        individual_value = human_penalize_extremes(individual, individual_value, environment.data)
    else:
        individual_value = generic_value_function(individual, environment.data)
        individual_value = generic_penalize_extremes(individual, individual_value, environment.data)
    individual["value"] = individual_value
    current_population[f"{environment.name}_{iteration}_filtered"].append(individual)
    return individual_value


def generic_value_function(individual, environment):
    """
    This method checks how good are the individual parameters
    :param individual: current individual parameters
    :type individual: dict
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: evaluation result
    :rtype: float
    """
    return sum([GENERIC_WEIGHTS[param] * min(value / environment[param], 1)
                if param not in ["_id", "age", "value"] else 0
                for param, value in individual.items()])


def generic_penalize_extremes(individual, total_value, environment):
    for param, value in individual.items():
        if param not in ["_id", "age", "value"] and value / environment[param] > 1.2:
            total_value = total_value * 0.5
    return total_value


def human_value_function(individual, environment):
    """
    This method checks how good are the individual parameters
    :param individual: current individual parameters
    :type individual: dict
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: evaluation result
    :rtype: float
    """
    skin_threshold = 0.05 + (abs(environment["temperature"] - 20) * 0.01)
    total_reach = individual["height"] + individual["arm_length"] + individual["jump"]

    total_value = 0
    total_value += (HUMAN_WEIGHTS["height"] +
                    HUMAN_WEIGHTS["jump"] +
                    HUMAN_WEIGHTS["arm_length"]) * min(total_reach / environment["tree_height"], 1)
    total_value += HUMAN_WEIGHTS["strength"] * min(individual["strength"] / environment["food_animals_strength"], 1)
    total_value += HUMAN_WEIGHTS["speed"] * min(individual["speed"] / environment["predators_speed"], 1)
    total_value += HUMAN_WEIGHTS["skin_thickness"] * min(individual["skin_thickness"] / skin_threshold, 1)
    return total_value


def human_penalize_extremes(individual, total_value, environment):
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
    skin_threshold = 0.05 + abs(environment["temperature"] - 20) * 0.01
    ind_speed_vs_predator = individual["speed"] / environment["predators_speed"]
    ind_speed_vs_food = individual["speed"] / environment["food_animals_speed"]
    ind_strength_vs_food = individual["strength"] / environment["food_animals_strength"]
    ind_skin_vs_temp = individual["skin_thickness"] / skin_threshold
    ind_reach_vs_trees = (individual["height"] +
                          individual["jump"] +
                          individual["arm_length"]) / environment["tree_height"]

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

    total_value = evaluate_fast_enough(individual, total_value, environment)
    total_value = evaluate_warm_enough(individual, total_value, environment)

    return total_value


def evaluate_fast_enough(individual, total_value, environment):
    """
    Check if the individual's speed is high enough to scape from predators. Otherwise, give a big penalization.
    :param individual: current individual parameters
    :type individual: dict
    :param total_value: current evaluation for the individual
    :type total_value: float
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: new evaluation for the individual
    :rtype: float
    """
    return total_value if is_fast_enough(individual, environment) else total_value * 0.2


def evaluate_warm_enough(individual, total_value, environment):
    """
    Check if the individual's skin is thick enough. Otherwise, give a big penalization.
    :param individual: current individual parameters
    :type individual: dict
    :param total_value: current evaluation for the individual
    :type total_value: float
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: new evaluation for the individual
    :rtype: float
    """
    return total_value if is_warm_enough(individual, environment) else total_value * 0.2


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
    return individual["speed"] >= environment["predators_speed"]


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
    return individual["strength"] > environment["food_animals_strength"]


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
    temp_threshold = 0.05 + (abs(environment["temperature"] - 20) * 0.01)
    return individual["skin_thickness"] > temp_threshold


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
    return is_tall_enough(individual, environment) or is_fast_and_strong_enough(individual, environment)


def is_fast_and_strong_enough(individual, environment):
    """
    This method checks if the individual can catch its preys and is strong enough to kill them.
    :param individual: current individual parameters
    :type individual: dict
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: true if the individual can hunt for food. false otherwise.
    :rtype: bool
    """
    return individual["speed"] > environment["food_animals_speed"] and \
        individual["strength"] > environment["food_animals_strength"]


def is_tall_enough(individual, environment):
    """
    This method checks if the individual can reach the food from the trees.
    :param individual: current individual parameters
    :type individual: dict
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: true if the individual can reach tree's food. false otherwise.
    :rtype: bool
    """
    return individual["height"] + individual["arm_length"] + individual["jump"] >= environment["tree_height"]


def show_best_and_worst_fitting(current_population, environment_name, iteration):
    """
    This method prints on terminal the best and worst valued individuals at a specific iteration
    :param current_population: set of individuals to test against the environment
    :param environment_name: the current parameters against which the individuals are being tested
    :type environment_name: str
    :type current_population: list or DBWrapper
    :param iteration: current iteration
    :type iteration: int
    """
    coll_name = f"{environment_name}_{iteration}"
    population = current_population[coll_name]
    logging.info(f"Worst individual in iteration {iteration}: {population[int(get_population_size() * 0.6) - 1]}")
    logging.info(f"Best individual in iteration {iteration}:  {population[0]}")
