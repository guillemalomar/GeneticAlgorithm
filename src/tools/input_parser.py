import argparse
import sys

from settings.generic_model import GENERIC_ENVIRONMENT_DEFAULT
from settings.human_model import HUMAN_ENVIRONMENT_DEFAULT
from settings.settings import max_iterations, elitism, mutation_factor, initial_population_size
from src import set_generic, set_elitist, set_mutation_factor, set_population_size
from src.tools import set_db
from src.tools.printers import show_about


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


def check_input(args):
    if args.about:
        show_about()
        sys.exit()
    if args.multiple and not args.name == "Not defined":
        print("The multiple flag has been activated, but a name for a single execution has been given.")
        print("Check your input parameters")
        sys.exit()
    if args.multiple and args.params != "Not defined":
        print("The multiple flag has been activated, but single parameters have been specified.")
        print("Check your input parameters")
        sys.exit()
    if args.params != "Not defined":
        try:
            print(args.params)
            exec_params = args.params.split(',')
            print(exec_params)
            args.params = [int(param) for param in exec_params]
        except TypeError:
            print("The format of params is incorrect.")
            sys.exit()
        if args.generic:
            if len(GENERIC_ENVIRONMENT_DEFAULT.keys()) != len(args.params):
                print("The number of params is incorrect.")
                sys.exit()
        else:
            if len(HUMAN_ENVIRONMENT_DEFAULT.keys()) != len(args.params):
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
        if args.generic:
            for ind, key in enumerate(GENERIC_ENVIRONMENT_DEFAULT.keys()):
                execution_params[key] = args.params[ind]
        else:
            for ind, key in enumerate(HUMAN_ENVIRONMENT_DEFAULT.keys()):
                execution_params[key] = args.params[ind]
    return execution_params


def set_globals(args):
    set_db(args.database)
    set_generic(args.generic)
    set_elitist(args.elitist)
    set_mutation_factor(args.mutationfactor)
    set_population_size(args.population)
