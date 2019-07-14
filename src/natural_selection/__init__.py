from settings import max_iterations
from src.natural_selection.filter import filter_individuals
from src.natural_selection.reproduct import obtain_children


def iterate():
    for i in range(0, max_iterations):
        filter_individuals()
        obtain_children()
