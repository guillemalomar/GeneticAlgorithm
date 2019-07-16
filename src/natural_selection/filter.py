from settings import ENVIRONMENT_PARAMS, initial_population_size


def filter_individuals(current_population):
    """
    Kill the worse fitting 2000 individuals
    :return:
    :rtype:
    """
    valued_individuals = []
    for individual in current_population:
        valued_individuals.append((individual, value_function(individual)))
    valued_individuals = [y[0] for y in sorted(valued_individuals, key=lambda x: x[1])]
    return valued_individuals[2000:]


def value_function(individual):
    """

    :param individual:
    :type individual:
    :return:
    :rtype:
    """
    total_value = 0
    total_value += \
        max((individual.height + individual.arm_length + individual.jump) / ENVIRONMENT_PARAMS['fruit_tree_height'], 1)
    total_value += \
        max(individual.speed / ENVIRONMENT_PARAMS['food_animals_speed'], 1)
    total_value += \
        max(individual.strength / ENVIRONMENT_PARAMS['food_animals_strength'], 1)
    # total_value += \
    #     individual.skin_thickness
    if (individual.height + individual.arm_length + individual.jump) < ENVIRONMENT_PARAMS['fruit_tree_height'] or \
       individual.speed < ENVIRONMENT_PARAMS['food_animals_speed'] or \
       individual.strength < ENVIRONMENT_PARAMS['food_animals_strength']:
        total_value = total_value * 0.5
    if individual.speed < ENVIRONMENT_PARAMS['predators_speed']:
        total_value = total_value * 0.2
    return total_value


def natural_death(iteration, current_population):
    """
    Kill all individuals which have as age the current iteration
    :return:
    :rtype:
    """
    young_individuals = []
    for individual in current_population:
        if individual.age > iteration:
            young_individuals.append(individual)
    return young_individuals[0: initial_population_size]
