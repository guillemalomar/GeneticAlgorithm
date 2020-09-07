import operator

from src import get_population_size


def natural_death(iteration, current_population, environment_name):
    """
    Kill all individuals which have as age the current iteration.
    :param iteration: current iteration
    :type iteration: int
    :param current_population: Object containing the individuals collections
    :type current_population: DBWrapper
    :param environment_name: the current parameters against which the individuals are being tested
    :type environment_name: str
    :return: the individuals that survived the filtering stage
    :rtype: list or DBWrapper
    """
    coll_to_trim = current_population[f'{environment_name}_{iteration}_{"reproduction"}']
    new_col = current_population[f'{environment_name}_{iteration + 1}']
    coll_to_trim.sort(key=operator.itemgetter('age'), reverse=True)
    for idx, individual in enumerate(coll_to_trim):
        if idx < get_population_size():
            individual['_id'] = idx
            new_col.append(individual)
    return current_population
