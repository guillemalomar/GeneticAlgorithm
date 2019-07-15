from src.natural_selection.populate import create_individuals
from src.natural_selection import iterate
from src.tools.plot import plot_results

if __name__ == '__main__':
    current_population = create_individuals()
    iterate(current_population)
    plot_results()
