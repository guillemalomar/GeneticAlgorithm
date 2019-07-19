max_iterations = 100
initial_population_size = 10000
mutation_factor = 0.02

INDIVIDUALS_PARAMS = {
    'height': [1, 1.5],
    'arm_length': [0, 0.5],
    'speed': [10, 20],
    'strength': [1, 10],
    'jump': [0, 0.5],
    'skin_thickness': [0.05, 2]
}

ENVIRONMENTS = {
    'Bayou': {
        'tree_height': 1.5,
        'temperature': 20,
        'predators_speed': 17,
        'food_animals_speed': 10,
        'food_animals_strength': 5
    },
    'Tundra': {
        'tree_height': 4,
        'temperature': -10,
        'predators_speed': 18,
        'food_animals_speed': 15,
        'food_animals_strength': 7
    },
    'Savannah': {
        'tree_height': 2.5,
        'temperature': 25,
        'predators_speed': 15,
        'food_animals_speed': 30,
        'food_animals_strength': 8
    },
    'Badlands': {
        'tree_height': 4,
        'temperature': 30,
        'predators_speed': 20,
        'food_animals_speed': 20,
        'food_animals_strength': 10
    }
}

ENVIRONMENT_DEFAULT = {
    'tree_height': 1.0,
    'temperature': 20.0,
    'predators_speed': 10.0,
    'food_animals_speed': 10.0,
    'food_animals_strength': 1.0
}