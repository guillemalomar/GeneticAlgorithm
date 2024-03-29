from src.natural_selection.filter import is_fast_enough, is_warm_enough
from settings.generic_model import GENERIC_PARAMS, GENERIC_ENVIRONMENT_DEFAULT
from src.tools import my_plot
from src import is_generic, get_population_size


class PopulationAnalysis:
    def __init__(self, environment, iteration):
        if is_generic():
            self.averages = {}
            for param in GENERIC_PARAMS.keys():
                self.averages[param] = 0
            self.averages["fitting"] = 0
            self.averages["value"] = 0
        else:
            self.averages = {
                "speed": 0,
                "strength": 0,
                "skin": 0,
                "total_reach": 0,
                "fitting": 0,
                "value": 0
            }
        self.__environment = environment
        self.iteration = iteration

    def analyze_population(self, current_population, environment_name, iteration):
        """
        This method obtains the averages for the current iteration individuals and saves the results to be plot
        :param current_population: current set of individuals
        :type current_population: list or DBWrapper
        :param environment_name: the current parameters against which the individuals are being tested
        :type environment_name: str
        :param iteration: current iteration
        :type iteration: int
        """
        coll_name = f"{environment_name}_{iteration + 1}"
        if not is_generic():
            total_speed, total_strength, total_skin, total_reach, total_value = 0, 0, 0, 0, 0
            to_evaluate = 0
            total_fitting = 0
            for individual in current_population[coll_name]:
                total_speed += individual["speed"]
                total_strength += individual["strength"]
                total_skin += individual["skin_thickness"]
                if "value" in individual:
                    total_value += individual["value"]
                    to_evaluate += 1
                reach = individual["height"] + individual["arm_length"] + individual["jump"]
                total_reach += reach
                if (reach > self.__environment["tree_height"] or
                    (individual["speed"] > self.__environment["food_animals_speed"] and
                     individual["strength"] > self.__environment["food_animals_strength"])) and \
                        is_fast_enough(individual, self.__environment) and \
                        is_warm_enough(individual, self.__environment):
                    total_fitting += 1
            self.averages = {
                "speed": total_speed / get_population_size(),
                "strength": total_strength / get_population_size(),
                "skin": total_skin / get_population_size(),
                "total_reach": total_reach / get_population_size(),
                "value": total_value / to_evaluate,
                "fitting": total_fitting
            }
        else:
            total_value = 0
            evaluated = 0
            for individual in current_population[coll_name]:
                fits = True
                for param, value in individual.items():
                    if param not in ["_id", "age", "value"]:
                        self.averages[param] += value
                        if fits and \
                           not (GENERIC_ENVIRONMENT_DEFAULT[param]-2 < value < GENERIC_ENVIRONMENT_DEFAULT[param]+2):
                            fits = False
                    if param == "value":
                        total_value += value
                        evaluated += 1
                if fits:
                    self.averages["fitting"] += 1
            self.averages["value"] = total_value / max(evaluated, 1)
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
        if self.averages["fitting"] >= int(get_population_size() * 0.80):
            total_difference = 0
            for key, val in self.averages.items():
                total_difference += abs(val - prev_analysis.averages[key])
            if total_difference < 0.1:
                return True
        if self.averages["fitting"] >= int(get_population_size() * 0.95):
            return True
        return False
