import logging

from src.natural_selection.filter import filter_individuals, natural_death
from src.natural_selection.reproduce import reproduction_stage
from src.tools.analyze import PopulationAnalysis


def iterate(max_iterations, current_population, environment):

    iteration = 0
    prev_analysis = PopulationAnalysis(environment[1], iteration)

    for iteration in range(1, max_iterations+1):

        if iteration % max(int(max_iterations / 10), 10) == 0:
            logging.info("Iteration: {}".format(iteration))

        current_population = filter_individuals(current_population, environment[1])

        current_population = reproduction_stage(iteration, current_population)

        current_population = natural_death(iteration, current_population)

        new_analysis = PopulationAnalysis(environment[1], iteration)
        new_analysis.analyze_population(current_population)

        if new_analysis.check_converged(prev_analysis):
            logging.info("Converged")
            break
        prev_analysis = new_analysis

    logging.info("Total number of iterations: {}".format(iteration))
    return current_population
