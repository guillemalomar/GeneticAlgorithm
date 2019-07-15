from settings import max_iterations
from src.natural_selection.filter import filter_individuals
from src.natural_selection.reproduct import reproduction_stage


def iterate():
    for i in range(1, max_iterations+1):
        filter_individuals()
        reproduction_stage(i)
