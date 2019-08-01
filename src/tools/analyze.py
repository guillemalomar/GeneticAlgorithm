from src.natural_selection.filter import is_fast_enough, is_warm_enough
from settings.generic_model import GENERIC_PARAMS, GENERIC_ENVIRONMENT_DEFAULT
from src.tools import my_plot
from src import is_generic, get_population_size


class PopulationAnalysis:
    def __init__(self, environment, iteration):
        if is_generic():
            self.averages = {}
            for param, _ in GENERIC_PARAMS.items():
                self.averages[param] = 0
            self.averages['fitting'] = 0
        else:
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
        if not is_generic():
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
                'avg_speed': total_speed / get_population_size(),
                'avg_strength': total_strength / get_population_size(),
                'avg_skin': total_skin / get_population_size(),
                'total_reach': total_reach / get_population_size(),
                'fitting': total_fitting
            }
        else:
            total_fitting = 0
            for individual in current_population:
                fits = True
                for param, value in individual.items():
                    if param != '_id' and param != 'age' and param != 'value':
                        self.averages[param] += value
                        if fits and value < GENERIC_ENVIRONMENT_DEFAULT[param]:
                            fits = False
                if fits:
                    total_fitting += 1
            self.averages['fitting'] = total_fitting
            for param, value in GENERIC_PARAMS.items():
                self.averages[param] = self.averages[param] / get_population_size()
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
        if self.averages['fitting'] >= int(get_population_size() * 0.85):
            total_dif = 0
            for key, val in self.averages.items():
                total_dif += abs(val - prev_analysis.averages[key])
            if total_dif < 2:
                return True
        if self.averages['fitting'] >= int(get_population_size() * 0.95):
            return True
        return False
