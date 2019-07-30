import argparse
import logging
import sys

from src.natural_selection.populate import create_individuals
from src.natural_selection import iterate
from src.tools import my_plot, set_db
from settings.settings import ENVIRONMENTS, ENVIRONMENT_DEFAULT, max_iterations
from settings.logger import set_logger

set_logger()


def args_handler(argv):
    """
    Input arguments processor.
    :param argv: the object containing the input parameters
    :type argv: argparse object
    :return: parsed arguments
    :rtype: a list of the final application input parameters
    """
    p = argparse.ArgumentParser(
        description='Genetic Algorithm',
        formatter_class=argparse.RawTextHelpFormatter
    )

    p.add_argument('-i', '--iterations', action='store', type=int,
                   default=max_iterations,
                   help='Number of iterations to run.')

    p.add_argument('-db', '--db', action='store_true',
                   default=False,
                   help='Use MongoDB.')

    p.add_argument('-a', '--about', action='store_true',
                   default=False,
                   help='Some information about the code.')

    p.add_argument('-c', '--custom', action='store_true',
                   default=False,
                   help='Flag to activate custom mode, to use environment parameters given by the user.')

    p.add_argument('-n', '--name', action='store', type=str,
                   default='Custom',
                   help='Name of the custom execution.')

    p.add_argument('-th', '--tree_height', action='store', type=float,
                   default=ENVIRONMENT_DEFAULT['tree_height'],
                   help='The environment trees height.')

    p.add_argument('-t', '--temperature', action='store', type=float,
                   default=ENVIRONMENT_DEFAULT['temperature'],
                   help='The environment temperature.')

    p.add_argument('-ps', '--predators_speed', action='store', type=float,
                   default=ENVIRONMENT_DEFAULT['predators_speed'],
                   help='The speed of the environment predators.')

    p.add_argument('-asp', '--food_animals_speed', action='store', type=float,
                   default=ENVIRONMENT_DEFAULT['food_animals_speed'],
                   help='The speed of the animals that the individuals can hunt.')

    p.add_argument('-ast', '--food_animals_strength', action='store', type=float,
                   default=ENVIRONMENT_DEFAULT['food_animals_strength'],
                   help='The strength of the animals that the individuals can hunt.')

    return p.parse_args(argv[1:])


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
    logging.info(20 * "#" + " NEW EXECUTION " + 20 * "#" + "\n" +
                 33*"#" + " Executing with the following parameters:\n" +
                 33*"#" + " Environment name: {}\n" + 33*"#" + " -".format(environment_name) +
                 "\n################################# -".join(
                     ['{}: {}'.format(key, value) for key, value in environment_params.items()])
                 )
    my_plot.add_limits(environment_params)
    logging.info("*** Population stage ***")
    initial_population = create_individuals(environment_name)
    logging.info("*** Iteration stage ***")
    iterate(maximum_iterations, initial_population, (environment_name, environment_params))
    logging.info("*** Closing stage ***")
    my_plot.save_results('{}'.format(environment_name))


def _main(argv):

    args = args_handler(argv)

    if args.about:
        print(30 * "#" + " Genetic Algorithm " + 31 * "#")
        print("# This project is an example of the most classic Genetic Algorithm problem.    # \n" +
              "# It will obtain 1 or more environments, will create a set of individuals with # \n" +
              "# random parameters values within a specified range, and will see how these    # \n" +
              "# parameters change with the iterations.                                       # \n")
        print(80 * "#")
        sys.exit()

    set_db(args.db)

    if args.custom:
        environment_name = args.name
        environment_params = {
            'tree_height': args.tree_height,
            'temperature': args.temperature,
            'predators_speed': args.predators_speed,
            'food_animals_speed': args.food_animals_speed,
            'food_animals_strength': args.food_animals_strength
        }
        execute_genetic_algorithm(args.iterations, environment_name, environment_params)
    else:
        for environment_name, environment_params in ENVIRONMENTS.items():
            execute_genetic_algorithm(args.iterations, environment_name, environment_params)
            my_plot.__init__()


if __name__ == '__main__':
    try:
        _main(sys.argv)
    except (KeyboardInterrupt, SystemExit):
        print("\nExecution cancelled manually")
        logging.info("Execution cancelled")
        sys.exit()
