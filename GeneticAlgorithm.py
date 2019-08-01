import logging
import sys

from settings.human_model import HUMAN_ENVIRONMENTS
from settings.generic_model import GENERIC_ENVIRONMENTS
from src.natural_selection.populate import create_individuals
from src.natural_selection import iterate
from src.tools import my_plot
from src.tools.printers import execution_message
from src.tools.input_parser import args_handler, check_input, set_defaults, fix_undefined, set_globals

from settings.logger import set_logger

set_logger()


def execute_genetic_algorithm(maximum_iterations, environment_name, environment_params):
    """
    Main genetic algorithm method
    :param maximum_iterations: limit number of iterations
    :type maximum_iterations: int
    :param environment_name: name of the environment
    :type environment_name: str
    :param environment_params: the current parameters against which the individuals will be tested
    :type environment_params: dict
    """
    my_plot.set_plots()
    execution_message(environment_name, environment_params)
    my_plot.add_limits(environment_params)
    logging.info("*** Population stage ***")
    initial_population = create_individuals(environment_name)
    logging.info("*** Iteration stage ***")
    iterate(maximum_iterations, initial_population, (environment_name, environment_params))
    logging.info("*** Closing stage ***")
    my_plot.save_results('{}'.format(environment_name))
    my_plot.__init__()


def _main(argv):

    args = args_handler(argv)
    args = check_input(args)
    set_globals(args)

    if not args.multiple:
        args = fix_undefined(args)
        environment_name = args.name
        environment_params = set_defaults(args)
        execute_genetic_algorithm(args.iterations, environment_name, environment_params)
    else:
        if args.generic:
            for environment_name, environment_params in GENERIC_ENVIRONMENTS.items():
                execute_genetic_algorithm(args.iterations, environment_name, environment_params)
        else:
            for environment_name, environment_params in HUMAN_ENVIRONMENTS.items():
                execute_genetic_algorithm(args.iterations, environment_name, environment_params)


if __name__ == '__main__':
    try:
        _main(sys.argv)
    except KeyboardInterrupt:
        print("\nExecution cancelled manually")
        logging.info("Execution cancelled manually")
        sys.exit()
