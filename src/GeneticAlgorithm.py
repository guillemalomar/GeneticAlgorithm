from src.natural_selection.populate import create_individuals
from src.natural_selection import iterate
from src.tools import my_plot

if __name__ == '__main__':
    current_population = create_individuals()
    current_population = iterate(current_population)
    my_plot.save_results('Result')
