import argparse
import logging
import sys

from src.natural_selection.populate import create_individuals
from src.natural_selection import iterate
from src.tools import my_plot, set_db
from settings.settings import ENVIRONMENTS, ENVIRONMENT_DEFAULT, max_iterations
from settings.logger import set_logger

set_logger()

NOT_DEFINED = -99999999


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

    p.add_argument('-a', '--about', action='store_true',
                   default=False,
                   help='(flag) obtain a breve about the application')

    p.add_argument('-db', '--database', action='store_true',
                   default=False,
                   help='(flag) activate MongoDB')

    p.add_argument('-c', '--custom', action='store_true',
                   default=False,
                   help='(flag) activate custom mode, to use environment parameters given by the user')

    p.add_argument('-n', '--name', action='store', type=str,
                   default="Not defined",
                   help='(text) name of the custom execution')

    p.add_argument('-th', '--tree_height', action='store', type=float,
                   default=NOT_DEFINED,
                   help='(float) the custom environment trees height')

    p.add_argument('-t', '--temperature', action='store', type=float,
                   default=NOT_DEFINED,
                   help='(float) the custom environment temperature')

    p.add_argument('-ps', '--predators_speed', action='store', type=float,
                   default=NOT_DEFINED,
                   help='(float) the custom environment predators speed')

    p.add_argument('-asp', '--food_animals_speed', action='store', type=float,
                   default=NOT_DEFINED,
                   help='(float) the custom environment speed of the animals that the individuals can hunt')

    p.add_argument('-ast', '--food_animals_strength', action='store', type=float,
                   default=NOT_DEFINED,
                   help='(float) the custom environment strength of the animals that the individuals can hunt')

    p.add_argument('-i', '--iterations', action='store', type=int,
                   default=max_iterations,
                   help='(integer) number of iterations to run')

    return p.parse_args(argv[1:])


def show_about():
    print(30 * "#" + " Genetic Algorithm " + 31 * "#")
    print("# This project is an example of the most classic Genetic Algorithm problem.    #\n" +
          "# It will obtain 1 or more environments, will create a set of individuals with #\n" +
          "# random parameters values within a specified range, and will see how these    #\n" +
          "# parameters change when facing the individuals against the environments over  #\n" +
          "# many iterations.                                                             #")
    print(80 * "#")


def execution_message(environment_name, environment_params):
    msg = 20 * "#" + " NEW EXECUTION " + 20 * "#" + "\n" + \
          33*"#" + " Executing with the following parameters:\n" +\
          33*"#" + " Environment name: {}\n".format(environment_name) + 33*"#" + " -" +\
          "\n################################# -".join(
              ['{}: {}'.format(key, value) for key, value in environment_params.items()])
    print(msg)
    logging.info(msg)


def check_input(args):
    if not args.custom and \
            (not args.name == "Not defined" or
             not args.temperature == NOT_DEFINED or
             not args.tree_height == NOT_DEFINED or
             not args.food_animals_strength == NOT_DEFINED or
             not args.food_animals_speed == NOT_DEFINED or
             not args.predators_speed == NOT_DEFINED):
        print("The custom flag hasn't been activated, but custom parameters have been specified.")
        print("Check your input parameters")
        sys.exit()


def set_defaults(args):
    if args.name == "Not defined":
        args.name = 'Custom'
    if args.temperature == NOT_DEFINED:
        args.temperature = ENVIRONMENT_DEFAULT['temperature']
    if args.tree_height == NOT_DEFINED:
        args.tree_height = ENVIRONMENT_DEFAULT['tree_height']
    if args.food_animals_strength == NOT_DEFINED:
        args.food_animals_strength = ENVIRONMENT_DEFAULT['food_animals_strength']
    if args.food_animals_speed == NOT_DEFINED:
        args.food_animals_speed = ENVIRONMENT_DEFAULT['food_animals_speed']
    if args.predators_speed == NOT_DEFINED:
        args.predators_speed = ENVIRONMENT_DEFAULT['predators_speed']


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
    execution_message(environment_name, environment_params)
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
        show_about()
        sys.exit()

    check_input(args)

    set_defaults(args)

    set_db(args.database)

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
    except KeyboardInterrupt:
        print("\nExecution cancelled manually")
        logging.info("Execution cancelled manually")
        sys.exit()
