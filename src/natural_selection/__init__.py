import logging

from src.natural_selection.filter import filter_individuals, natural_death
from src.natural_selection.reproduce import reproduction_stage
from src.tools.analyze import PopulationAnalysis
from src.tools import check_and_return_db


def iterate(max_iterations, current_population, environment):

    iteration = 0
    prev_analysis = PopulationAnalysis(environment[1], iteration)

    for iteration in range(1, max_iterations+1):

        if iteration % max(int(max_iterations / 10), 10) == 0:
            logging.info("Iteration: {}".format(iteration))

        if check_and_return_db():
            if iteration > 1:
                check_and_return_db().delete_collection(environment[0], iteration - 1)
                check_and_return_db().create_collection(environment[0], iteration)
                check_and_return_db().insert_documents_into_collection(environment[0], iteration, current_population)
            current_population = check_and_return_db().obtain_all_documents(environment[0], iteration)

        current_population = filter_individuals(current_population, environment[1])

        current_population = reproduction_stage(iteration, current_population)

        current_population = natural_death(iteration, current_population)

        analysis = PopulationAnalysis(environment[1], iteration)
        analysis.analyze_population(current_population)

        if analysis.check_converged(prev_analysis):
            logging.info("Converged")
            break
        prev_analysis = analysis

    logging.info("Total number of iterations: {}".format(iteration))
    return current_population
