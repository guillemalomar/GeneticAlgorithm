import argparse
import logging
import sys

from src.natural_selection.populate import create_individuals
from src.natural_selection import iterate
from src import set_generic, set_elitist, set_mutation_factor, set_population_size
from src.tools import my_plot, set_db
from settings.human_model import HUMAN_ENVIRONMENTS, HUMAN_ENVIRONMENT_DEFAULT
from settings.generic_model import GENERIC_ENVIRONMENT_DEFAULT, GENERIC_ENVIRONMENTS
from settings.settings import max_iterations, elitism, mutation_factor, initial_population_size
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

    p.add_argument('-a', '--about', action='store_true',
                   default=False,
                   help='(flag) obtain a breve about the application')

    p.add_argument('-db', '--database', action='store_true',
                   default=False,
                   help='(flag) activate MongoDB')

    p.add_argument('-g', '--generic', action='store_true',
                   default=False,
                   help='(flag) activate generic mode, to use the parameters in the settings/generic_model.py file')

    p.add_argument('-n', '--name', action='store', type=str,
                   default="Not defined",
                   help='(text) name of the single execution')

    p.add_argument('-p', '--params', action='store', type=str,
                   default="Not defined",
                   help='(text) comma separated parameters for the single execution')

    p.add_argument('-m', '--multiple', action='store_true',
                   default=False,
                   help='(flag) activate multiple mode, to execute many environments at once')

    p.add_argument('-e', '--elitist', action='store_true',
                   default=elitism,
                   help='(flag) pair individuals with other with a similar fitness value, instead of randomly')

    p.add_argument('-pop', '--population', action='store', type=int,
                   default=initial_population_size,
                   help='(int) initial population size')

    p.add_argument('-i', '--iterations', action='store', type=int,
                   default=max_iterations,
                   help='(integer) number of iterations to run')

    p.add_argument('-mf', '--mutationfactor', action='store', type=float,
                   default=mutation_factor,
                   help='(float) mutation factor')

    return p.parse_args(argv[1:])


def show_about():
    print(30 * "#" + " Genetic Algorithm " + 31 * "#")
    print("# This project is an example of the most classic Genetic Algorithm problem.    #\n" +
          "# The "
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
    if args.multiple and not args.name == "Not defined":
        print("The multiple flag has been activated, but a name for a single execution has been given.")
        print("Check your input parameters")
        sys.exit()
    if args.multiple != "Not defined" and args.params != "Not defined":
        print("The multiple flag has been activated, but single parameters have been specified.")
        print("Check your input parameters")
        sys.exit()
    if args.params != "Not defined":
        try:
            exec_params = args.params.split(',')
            _ = [int(param) for param in exec_params]
        except TypeError:
            print("The format of params is incorrect.")
            sys.exit()
        for param in exec_params:
            if type(param) is not int:
                print("The format of params is incorrect.")
        if args.generic:
            if len(GENERIC_ENVIRONMENT_DEFAULT.keys()) != len(exec_params):
                print("The number of params is incorrect.")
                sys.exit()
        else:
            if len(HUMAN_ENVIRONMENT_DEFAULT.keys()) != len(exec_params):
                print("The number of params is incorrect.")
                sys.exit()
    return args


def fix_undefined(args):
    if not args.multiple and args.name == "Not defined":
        if args.generic:
            args.name = "Generic Execution"
        else:
            args.name = "Human Execution"
    return args


def set_defaults(args):
    if args.generic:
        execution_params = GENERIC_ENVIRONMENT_DEFAULT
    else:
        execution_params = HUMAN_ENVIRONMENT_DEFAULT
    if not args.multiple and args.params != "Not defined":
        exec_params = args.params.split(',')
        if args.generic:
            for ind, key in enumerate(GENERIC_ENVIRONMENT_DEFAULT.keys()):
                execution_params[key] = exec_params[ind]
        else:
            for ind, key in enumerate(HUMAN_ENVIRONMENT_DEFAULT.keys()):
                execution_params[key] = exec_params[ind]
    return execution_params


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

    if args.about:
        show_about()
        sys.exit()

    args = check_input(args)

    set_db(args.database)
    set_generic(args.generic)
    set_elitist(args.elitist)
    set_mutation_factor(args.mutationfactor)
    set_population_size(args.population)

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
