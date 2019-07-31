from src.natural_selection.filter import is_fast_enough, is_warm_enough
from settings.settings import initial_population_size
from src.tools import my_plot


class PopulationAnalysis:
    def __init__(self, environment, iteration):
        self.averages = {
            'avg_speed': 0,
            'avg_strength': 0,
            'avg_skin': 0,
            'total_reach': 0,
            'fitting': 0
        }
        self.environment = environment
        self.iteration = iteration

    def analyze_population(self, current_population):
        """
        This method obtains the averages for the current iteration individuals and saves the results to be plot
    :param current_population: current set of individuals
    :type current_population: list or DBWrapper
        """
        total_speed = 0
        total_strength = 0
        total_skin = 0
        total_reach = 0
        total_fitting = 0
        for individual in current_population:
            total_speed += individual['speed']
            total_strength += individual['strength']
            total_skin += individual['skin_thickness']
            reach = individual['height'] + individual['arm_length'] + individual['jump']
            total_reach += reach
            if (reach > self.environment['tree_height'] or
                (individual['speed'] > self.environment['food_animals_speed'] and
                 individual['strength'] > self.environment['food_animals_strength'])) and \
                    is_fast_enough(individual, self.environment) and \
                    is_warm_enough(individual, self.environment):
                total_fitting += 1
        self.averages = {
            'avg_speed': total_speed / initial_population_size,
            'avg_strength': total_strength / initial_population_size,
            'avg_skin': total_skin / initial_population_size,
            'total_reach': total_reach / initial_population_size,
            'fitting': total_fitting
        }
        my_plot.add_data(self.averages, self.iteration)

    def check_converged(self, prev_analysis):
        """
        This method checks if the current iteration individuals have changed much compared to the previous
        iteration individuals
        :param prev_analysis: the previous iteration individuals average parameters
        :type prev_analysis: PopulationAnalysis object
        :return: true if the current iteration individual parameters are really similar to the previous one. false
        otherwise
        :rtype: boolean
        """
        if self.averages['fitting'] >= int(initial_population_size * 0.9):
            total_dif = 0
            for key, val in self.averages.items():
                total_dif += abs(val - prev_analysis.averages[key])
            if total_dif < 0.5:
                return True
        return False
