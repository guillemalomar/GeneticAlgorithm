from settings import max_iterations
from src.natural_selection.filter import filter_individuals, natural_death
from src.natural_selection.reproduct import reproduction_stage
from src.tools.analyze import analyze_population


def iterate(current_population):
    max_iterations = 100
    for iteration in range(1, max_iterations+1):
        current_population = filter_individuals(current_population)
        current_population = reproduction_stage(iteration, current_population)
        current_population = natural_death(iteration, current_population)
        if iteration % 5 == 1:
            analyze_population(current_population)
