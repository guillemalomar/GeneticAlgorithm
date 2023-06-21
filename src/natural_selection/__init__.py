import logging

from src.natural_selection.filter import filter_individuals, show_best_and_worst_fitting
from src.natural_selection.reproduce import reproduction_stage
from src.natural_selection.natural_death import natural_death
from src.tools.analyze import PopulationAnalysis

iteration = 0


def iterate(max_iterations, current_population, environment):
    """
    Main iteration loop.
    :param max_iterations: maximum number of iterations in case of non-convergence
    :type max_iterations: int
    :param current_population: starting set of individuals to test against the environment
    :type current_population: list or DBWrapper
    :param environment: the current parameters against which the individuals will be tested
    :type environment: Environment
    :return: final individuals after reaching max_iterations or converging
    :rtype: list or DBWrapper
    """
    global iteration
    prev_analysis = PopulationAnalysis(environment.data, iteration)

    while True:
        iteration += 1

        if iteration >= max_iterations:
            break

        current_population = filter_individuals(current_population, environment, iteration)
        if iteration % 5 == 0:
            show_best_and_worst_fitting(current_population, environment.name, iteration)

        current_population = reproduction_stage(iteration, current_population, environment.name)

        current_population = natural_death(iteration, current_population, environment.name)

        del current_population[f"{environment.name}_{iteration}"]
        del current_population[f"{environment.name}_{iteration}_filtered"]
        del current_population[f"{environment.name}_{iteration}_reproduction"]

        new_analysis = PopulationAnalysis(environment.data, iteration)
        new_analysis.analyze_population(current_population, environment.name, iteration)

        if new_analysis.check_converged(prev_analysis):
            logging.info("Converged")
            break
        prev_analysis = new_analysis

    logging.info(f"Total number of iterations: {iteration}")
    iteration = 0
    return current_population
