import logging

from src.natural_selection.filter import filter_individuals, show_best_and_worst_fitting
from src.natural_selection.reproduce import reproduction_stage
from src.natural_selection.natural_death import natural_death
from src.tools.analyze import PopulationAnalysis


def iterate(max_iterations, current_population, environment):
    """
    Main iteration loop.
    :param max_iterations: maximum number of iterations in case of non-convergence
    :type max_iterations: int
    :param current_population: starting set of individuals to test against the environment
    :type current_population: list or DBWrapper
    :param environment: the current parameters against which the individuals will be tested
    :type environment: dict
    :return: final individuals after reaching max_iterations or converging
    :rtype: list or DBWrapper
    """
    iteration = 0
    prev_analysis = PopulationAnalysis(environment[1], iteration)

    for iteration in range(1, max_iterations+1):

        current_population = filter_individuals(current_population, environment[1])
        if iteration % 5 == 0:
            show_best_and_worst_fitting(current_population, iteration)

        current_population = reproduction_stage(iteration, current_population)

        current_population = natural_death(iteration, current_population)

        new_analysis = PopulationAnalysis(environment[1], iteration)
        new_analysis.analyze_population(current_population)

        if new_analysis.check_converged(prev_analysis):
            logging.info("Converged")
            break
        prev_analysis = new_analysis

    logging.info("Total number of iterations: {}".format(iteration))
    print("Total number of iterations: {}".format(iteration))
    return current_population
