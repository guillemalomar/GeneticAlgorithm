import logging
import sys

from src.environment import Environment
from src.natural_selection import iterate
from src.natural_selection.populate import create_individuals
from src.tools import my_plot
from src.tools.input_parser import process_args, obtain_environments
from src.tools.logger import set_logger
from src.tools.printers import execution_message

set_logger()


def execute_genetic_algorithm(maximum_iterations, environment):
    """
    Main genetic algorithm method
    :param maximum_iterations: limit number of iterations
    :type maximum_iterations: int
    :param environment: current environment
    :type environment: Environment
    """
    my_plot.set_plots()
    execution_message(environment)
    my_plot.add_limits(environment.data)
    logging.info("*** Population stage ***")
    initial_population = create_individuals(environment.name)
    logging.info("*** Iteration stage ***")
    iterate(maximum_iterations, initial_population, environment)
    logging.info("*** Closing stage ***")
    my_plot.save_results('{}'.format(environment.name))
    my_plot.__init__()


def _main(argv):
    """
    This method processes the input and runs the Genetic Algorithm for each input environment
    :param argv: input arguments
    :type argv: argv object
    """
    args = process_args(argv)
    for environment_name, environment_params in obtain_environments(args).items():
        environment = Environment(environment_name, environment_params)
        execute_genetic_algorithm(args.iterations, environment)


if __name__ == '__main__':
    try:
        _main(sys.argv)
    except KeyboardInterrupt:
        msg = "\nExecution cancelled manually"
        print("\n" + msg)
        logging.info(msg)
        sys.exit()
