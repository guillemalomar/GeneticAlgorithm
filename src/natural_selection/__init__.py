from settings import max_iterations
from src.natural_selection.filter import filter_individuals, natural_death
from src.natural_selection.reproduct import reproduction_stage
from src.tools.analyze import analyze_population
from src.tools import my_plot
from src.tools import my_mongo_wrapper


def iterate(current_population):
    for iteration in range(1, max_iterations+1):
        if iteration > 1:
            my_mongo_wrapper.create_collection(iteration)
            my_mongo_wrapper.insert_documents_into_collection(iteration, current_population)
        current_population = my_mongo_wrapper.obtain_all_documents(iteration)
        current_population = filter_individuals(current_population)
        current_population = reproduction_stage(iteration, current_population)
        current_population = natural_death(iteration, current_population)
        if iteration % 10 == 0:
            analysis = analyze_population(current_population)
            my_plot.add_data(analysis, iteration)
        else:
            my_mongo_wrapper.delete_collection(iteration)
    return current_population
