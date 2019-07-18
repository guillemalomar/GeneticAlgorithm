
def analyze_population(current_population, environment):
    total_height = 0
    total_speed = 0
    total_strength = 0
    total_arm = 0
    total_jump = 0
    total_skin = 0
    total_reach = 0
    total_not_fitting = 0
    for individual in current_population:
        total_height += individual['height']
        total_speed += individual['speed']
        total_strength += individual['strength']
        total_arm += individual['arm_length']
        total_jump += individual['jump']
        total_skin += individual['skin_thickness']
        total_reach += individual['height'] + individual['arm_length'] + individual['jump']
        if ((individual['height'] + individual['arm_length'] + individual['jump']) < environment['fruit_tree_height'] and
            (individual['speed'] < environment['food_animals_speed'] and
             individual['strength'] < environment['food_animals_strength'])) or \
           individual['speed'] < environment['predators_speed']:
            total_not_fitting += 1
    avgs = {
        'avg_height': total_height / len(current_population),
        'avg_speed': total_speed / len(current_population),
        'avg_strength': total_strength / len(current_population),
        'avg_arm': total_arm / len(current_population),
        'avg_jump': total_jump / len(current_population),
        'avg_skin': total_skin / len(current_population),
        'total_reach': total_reach / len(current_population),
        'not_fitting': total_not_fitting
    }
    return avgs
