
def analyze_population(current_population, environment):
    total_speed = 0
    total_strength = 0
    total_skin = 0
    total_reach = 0
    total_fitting = 0
    for individual in current_population:
        total_speed += individual['speed']
        total_strength += individual['strength']
        total_skin += individual['skin_thickness']
        total_reach += individual['height'] + individual['arm_length'] + individual['jump']
        if ((individual['height'] + individual['arm_length'] + individual['jump']) > environment['tree_height'] or
            (individual['speed'] > environment['food_animals_speed'] and
             individual['strength'] > environment['food_animals_strength'])) and \
           individual['speed'] > environment['predators_speed']:
            total_fitting += 1
    avgs = {
        'avg_speed': total_speed / len(current_population),
        'avg_strength': total_strength / len(current_population),
        'avg_skin': total_skin / len(current_population),
        'total_reach': total_reach / len(current_population),
        'fitting': total_fitting
    }
    return avgs
