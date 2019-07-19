import argparse
import sys

from src.natural_selection.populate import create_individuals
from src.natural_selection import iterate
from src.tools import my_plot, set_db
from settings import ENVIRONMENTS, ENVIRONMENT_DEFAULT, max_iterations


def args_handler(argv):

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


def _main(argv):

    args = args_handler(argv)

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
        my_plot.add_limits(environment_params)
        initial_population = create_individuals(environment_name)
        iterate(args.iterations, initial_population, (environment_name, environment_params))
        my_plot.save_results('{}'.format(environment_name))
    else:
        for environment_name, environment_params in ENVIRONMENTS.items():
            my_plot.add_limits(environment_params)
            initial_population = create_individuals(environment_name)
            iterate(args.iterations, initial_population, (environment_name, environment_params))
            my_plot.save_results('{}'.format(environment_name))
            my_plot.__init__()


if __name__ == '__main__':
    _main(sys.argv)
