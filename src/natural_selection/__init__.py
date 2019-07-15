from settings import max_iterations
from src.natural_selection.filter import filter_individuals, natural_death
from src.natural_selection.reproduct import reproduction_stage


def iterate(current_population):
    for i in range(1, max_iterations+1):
        current_population = filter_individuals(current_population)
        current_population = reproduction_stage(i, current_population)
        current_population = natural_death()
