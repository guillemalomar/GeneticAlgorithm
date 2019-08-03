generic_execution = False
elitist_order = False
mutation_factor = 0
initial_population_size = 100


def set_generic(to_activate):
    if to_activate:
        global generic_execution
        generic_execution = True


def is_generic():
    return generic_execution


def set_elitist(to_activate):
    if to_activate:
        global elitist_order
        elitist_order = True


def is_elitist():
    return elitist_order


def set_mutation_factor(mutation_factor_to_set):
    global mutation_factor
    mutation_factor = mutation_factor_to_set


def get_mutation_factor():
    return mutation_factor


def set_population_size(size_to_set):
    global initial_population_size
    initial_population_size = size_to_set


def get_population_size():
    return initial_population_size
