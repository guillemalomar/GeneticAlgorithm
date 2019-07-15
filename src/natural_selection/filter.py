from src import ENVIRONMENT
from settings import ENVIRONMENT_PARAMS


def filter_individuals(current_population):
    '''
    Kill the worse fitting 2000 individuals
    :return:
    :rtype:
    '''
    valued_individuals = []
    for individual in current_population:
        valued_individuals.append((individual, value_function(individual)))
    valued_individuals = [y[0] for y in sorted(valued_individuals, key=lambda x: x[1])]
    return valued_individuals[2000:]


def value_function(individual):
    total_value = 0
    total_value +=\
        (individual.height + individual.arm_length + individual.jump) / ENVIRONMENT_PARAMS['fruit_tree_height'] * 0.15
    total_value +=\
        individual.speed / ENVIRONMENT_PARAMS['food_animals_speed'] * 0.1
    total_value +=\
        individual.strength / ENVIRONMENT_PARAMS['food_animals_strength'] * 0.2
    total_value +=\
        ENVIRONMENT_PARAMS['predators_speed'] / individual.speed * 0.2
    total_value +=\
        individual.skin_thickness
    return total_value


def natural_death():
    '''
    Kill all individuals which have as age the current iteration
    :return:
    :rtype:
    '''
    pass
