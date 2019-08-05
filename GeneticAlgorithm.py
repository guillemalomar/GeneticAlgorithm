import logging
import sys

from src.environment import Environment
from src.natural_selection import iterate
from src.natural_selection.populate import create_individuals
from src.tools import my_plot
from src.tools.input_parser import process_args
from src.tools.logger import set_logger
from src.tools.printers import execution_message
from settings.settings import MESSAGES

set_logger()


def execute_genetic_algorithm(maximum_iterations, environment):
    """
    Main genetic algorithm method
    :param maximum_iterations: limit number of iterations
    :type maximum_iterations: int
    :param environment: current environment
    :type environment: Environment
    """
    my_plot.set_plots(environment)
    execution_message(environment)
    my_plot.add_limits(environment.data)
    logging.info(MESSAGES["POP_STAGE"])
    initial_population = create_individuals(environment.name)
    logging.info(MESSAGES["ITERATION_STAGE"])
    iterate(maximum_iterations, initial_population, environment)
    logging.info(MESSAGES["CLOSING_STAGE"])
    my_plot.save_results('{}'.format(environment.name))
    my_plot.__init__()


def _main(argv):
    """
    This method processes the input and runs the Genetic Algorithm for each input environment
    :param argv: input arguments
    :type argv: argv object
    """
    args = process_args(argv)
    for environment_name, environment_params in args.environments.items():
        environment = Environment(environment_name, environment_params)
        execute_genetic_algorithm(args.iterations, environment)


if __name__ == '__main__':
    try:
        _main(sys.argv)
    except KeyboardInterrupt:
        msg = "\n" + MESSAGES["CANCELLED_EXECUTION"]
        print("\n" + msg)
        logging.info(msg)
        sys.exit()
