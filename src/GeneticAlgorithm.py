from natural_selection.populate import create_individuals
from natural_selection import iterate
from tools.plot import plot_results

if __name__ == '__main__':
    create_individuals()
    iterate()
    plot_results()
