from settings import ENVIRONMENT_PARAMS, initial_population_size


def filter_individuals(current_population):
    """
    Kill the worse fitting 2000 individuals, depending on their parameters
    :param current_population:
    :type current_population: list of individuals
    :return:
    :rtype: list of individuals
    """
    valued_individuals = []
    for individual in current_population:
        individual_value = value_function(individual)
        individual_value = check_enough_food(individual, individual_value)
        individual_value = check_too_good(individual, individual_value)
        individual_value = check_fast_enough(individual, individual_value)
        valued_individuals.append((individual, individual_value))
    valued_individuals = [y[0] for y in sorted(valued_individuals, key=lambda x: x[1])]
    return valued_individuals[2000:]


def value_function(individual):
    """
    This method checks how good are the individual parameters
    :param individual:
    :type individual: Individual
    :return:
    :rtype: float
    """
    total_value = 0
    total_value += \
        (individual['height'] + individual['arm_length'] + individual['jump']) / ENVIRONMENT_PARAMS['fruit_tree_height']
    total_value += \
        min(individual['speed'] / ENVIRONMENT_PARAMS['food_animals_speed'],
            individual['strength'] / ENVIRONMENT_PARAMS['food_animals_strength'])
    # total_value += \
    #     individual['skin_thickness']
    return total_value


def check_enough_food(individual, total_value):
    """
    This method checks if the individual will be able to obtain food in some way. Otherwise is penalized.
    :param individual:
    :type individual: Individual
    :param total_value:
    :type total_value: float
    :return:
    :rtype: float
    """
    if (individual['total_reach'] < ENVIRONMENT_PARAMS['fruit_tree_height']) or \
        (individual['speed'] < ENVIRONMENT_PARAMS['food_animals_speed'] and
         individual['strength'] < ENVIRONMENT_PARAMS['food_animals_strength']):
        total_value = total_value * 0.5
    return total_value


def check_too_good(individual, total_value):
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
    ind_speed_vs_predator = individual['speed'] / ENVIRONMENT_PARAMS['predators_speed']
    ind_speed_vs_food = individual['speed'] / ENVIRONMENT_PARAMS['food_animals_speed']
    ind_strength_vs_food = individual['strength'] / ENVIRONMENT_PARAMS['food_animals_strength']

    if individual['total_reach'] / ENVIRONMENT_PARAMS['fruit_tree_height'] > 1.1:
        total_value = total_value * 0.80

    if ind_speed_vs_food > 1.1:
        total_value = total_value * 0.80
        if ind_strength_vs_food > 1.1:
            total_value = total_value * 0.80

    if ind_speed_vs_predator > 1.1:
        total_value = total_value * 0.80

    return total_value


def check_fast_enough(individual, total_value):
    """
    Check if the individual's speed is high enough to scape from predators. Otherwise give a big penalization.
    :param individual:
    :type individual: Individual
    :param total_value:
    :type total_value: float
    :return:
    :rtype: float
    """
    if individual['speed'] < ENVIRONMENT_PARAMS['predators_speed']:
        total_value = total_value * 0.2
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
    return young_individuals[0: initial_population_size]
