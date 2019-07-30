import asyncio
import logging

from settings.settings import initial_population_size


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
        valued_individuals = [y[0] for y in sorted(valued_individuals, key=lambda x: x[1])]
        valued_individuals = valued_individuals[int(initial_population_size * 0.4):]
        logging.debug("Deleted {} individuals".format(int(initial_population_size * 0.4)))
        return valued_individuals
    else:
        coll = current_population.current_collection
        valued_individuals = asyncio.run(create_evaluation_tasks(coll, environment))
        for individual in valued_individuals:
            coll[individual[0]['_id']] = individual[0]
        current_population.create_collection_and_set('{}_{}'.format(coll.name, 'filtered'))
        for it_id, item in enumerate(coll.find({},
                                               sort=[("${}".format("value"), -1)],
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
    individual_value = individual_value * 0.5 if not check_enough_food(individual, environment) else individual_value
    individual_value = check_too_good(individual, individual_value, environment)
    individual_value = check_fast_enough(individual, individual_value, environment)
    individual_value = check_warm_enough(individual, individual_value, environment)
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
    :param individual: current individual parameters
    :type individual: dict
    :param environment: the current parameters against which the individuals are being tested
    :type environment: dict
    :return: true if the individual has a way of finding food. false otherwise.
    :rtype: bool
    """
    if (individual['total_reach'] < environment['tree_height']) or \
        (individual['speed'] < environment['food_animals_speed'] and
         individual['strength'] < environment['food_animals_strength']):
        return False
    return True


def check_tall_enough(individual, environment):
    """

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


def check_strong_enough(individual, environment):
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


def check_fast_enough(individual, total_value, environment):
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
        total_value = total_value * 0.1
    else:
        total_value = total_value * 2
    return total_value


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


def check_warm_enough(individual, total_value, environment):
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
        total_value = total_value * 0.1
    else:
        total_value = total_value * 1.5
    return total_value


def natural_death(iteration, current_population):
    """
    Kill all individuals which have as age the current iteration.
    Also clean old database in case that we are using MongoDB
    :param iteration: current iteration
    :type iteration: int
    :param current_population: Object containing the individuals collections
    :type current_population: DBWrapper
    :return: the individuals that survived the filtering stage
    :rtype: list or DBWrapper
    """
    if type(current_population) is list:
        young_individuals = []
        for individual in current_population:
            if individual['age'] > iteration:
                young_individuals.append(individual)
        young_individuals = young_individuals[0: initial_population_size]
        logging.debug(
            "{} individuals died of natural causes".format(int(len(current_population) - len(young_individuals)))
        )
        return young_individuals
    else:
        reproduced_population = current_population.current_collection
        new_init_coll = '{}_{}'.format(reproduced_population.name.split('_')[0], iteration + 1)
        current_population.create_collection_and_set(new_init_coll)
        for index, individual in enumerate(reproduced_population.find({"age": {"$gt": iteration}})):
            individual['_id'] = index
            current_population.current_collection.insert_one(individual)

        current_population.clean_old_collections(reproduced_population.name)

        return current_population
