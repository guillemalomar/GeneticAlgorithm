import logging

from settings.settings import initial_population_size


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
