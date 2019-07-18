from src.natural_selection.populate import create_individuals
from src.natural_selection import iterate
from src.tools import my_plot
from settings import ENVIRONMENTS as environments

if __name__ == '__main__':
    for environment_name, environment_params in environments.items():
        initial_population = create_individuals(environment_name)
        fitting_population = iterate(initial_population, (environment_name, environment_params))
        my_plot.save_results('{}'.format(environment_name))
        my_plot.__init__()
