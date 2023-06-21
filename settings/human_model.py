HUMAN_PARAMS = {
    'height': [1, 1.5],
    'arm_length': [0, 0.5],
    'speed': [9, 10],
    'strength': [1, 10],
    'jump': [0, 0.5],
    'skin_thickness': [0.03, 0.05]
}

HUMAN_WEIGHTS = {
    'speed': 0.225,
    'strength': 0.225,
    'arm_length': 0.15,
    'jump': 0.15,
    'height': 0.2,
    'skin_thickness': 0.05
}

HUMAN_ENVIRONMENT_DEFAULT = {
    'tree_height': 2.0,
    'temperature': 20.0,
    'predators_speed': 10.0,
    'food_animals_speed': 10.0,
    'food_animals_strength': 8.0
}

HUMAN_ENVIRONMENTS = {
    'Bayou': {
        'tree_height': 1.5,
        'temperature': 20,
        'predators_speed': 17,
        'food_animals_speed': 10,
        'food_animals_strength': 5
    },
    'Tundra': {
        'tree_height': 2.75,
        'temperature': -5,
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
        'tree_height': 2.75,
        'temperature': 40,
        'predators_speed': 20,
        'food_animals_speed': 20,
        'food_animals_strength': 8
    }
}
