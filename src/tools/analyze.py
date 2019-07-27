from src.natural_selection.filter import is_fast_enough, is_warm_enough
from settings.settings import initial_population_size
from src.tools import my_plot


class PopulationAnalysis:
    def __init__(self):
        self.averages = {
            'avg_speed': 0,
            'avg_strength': 0,
            'avg_skin': 0,
            'total_reach': 0,
            'fitting': 0
        }

    def analyze_population(self, current_population, environment, iteration):
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
                    is_fast_enough(individual, environment) and \
                    is_warm_enough(individual, environment):
                total_fitting += 1
        self.averages = {
            'avg_speed': total_speed / len(current_population),
            'avg_strength': total_strength / len(current_population),
            'avg_skin': total_skin / len(current_population),
            'total_reach': total_reach / len(current_population),
            'fitting': total_fitting
        }
        my_plot.add_data(self.averages, iteration)


def check_converged(analysis1, analysis2):
    total_dif = 0
    for key, val in analysis1.averages.items():
        total_dif += abs(val - analysis2.averages[key])
    print(total_dif)
    if total_dif < 0.25 and analysis1.averages['fitting'] == initial_population_size:
        return True
    return False
