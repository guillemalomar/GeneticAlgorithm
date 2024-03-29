import logging
import matplotlib.pyplot as plt

from settings.generic_model import GENERIC_PARAMS
from settings.human_model import HUMAN_PARAMS
from settings.settings import max_iterations
from src import is_generic, get_population_size


class PlotWrapper:
    def __init__(self):
        self.__fig = plt.figure(figsize=(12, 9))
        self.__data = None
        self.__fitting = None
        self.__ax1 = None
        self.__ax2 = None
        self.__ax3 = None
        self.__ax4 = None
        self.__ax5 = None
        self.__ax6 = None

    def set_plots(self, environment):
        if not is_generic():
            temp_threshold = 0.05 + (abs(environment.data["temperature"] - 20) * 0.01)
            self.__ax1 = self.__fig.add_subplot(3, 2, 1)
            self.__ax1.set_title("Average Speed")
            self.__ax1.set_ylim([min(HUMAN_PARAMS["speed"][0] * 0.8, environment.data['predators_speed'] * 0.8,
                                     environment.data['food_animals_speed'] * 0.8),
                                 max(HUMAN_PARAMS["speed"][1] * 1.2, environment.data['predators_speed'] * 1.2,
                                     environment.data['food_animals_speed'] * 1.2)])
            self.__ax2 = self.__fig.add_subplot(3, 2, 2)
            self.__ax2.set_title("Average Strength")
            self.__ax2.set_ylim(
                [min(HUMAN_PARAMS["strength"][0] * 0.8, environment.data['food_animals_strength'] * 0.8),
                 max(HUMAN_PARAMS["strength"][1] * 1.2, environment.data['food_animals_strength'] * 1.2)])
            self.__ax3 = self.__fig.add_subplot(3, 2, 3)
            self.__ax3.set_title("Average Skin thickness")
            self.__ax3.set_ylim([min(HUMAN_PARAMS["skin_thickness"][0] * 0.8, temp_threshold * 0.8),
                                 max(HUMAN_PARAMS["skin_thickness"][1] * 1.2, temp_threshold * 1.2)])
            self.__ax4 = self.__fig.add_subplot(3, 2, 4)
            self.__ax4.set_title("Average Total Reach")
            self.__ax4.set_ylim([1 * 0.8, 2.5 * 1.2])
            self.__ax5 = self.__fig.add_subplot(3, 2, 5)
            self.__ax5.set_title("Individuals fitting")
            self.__ax5.set_ylim([(get_population_size() * 0.9) - get_population_size(), get_population_size() * 1.1])
            self.__ax6 = self.__fig.add_subplot(3, 2, 6)
        else:
            ind = 1
            num_attrs = len(environment.data.keys())
            num_rows = int((num_attrs + 2) / 2) + 1
            num_cols = 2
            for key, val in environment.data.items():
                self.__setattr__(key, self.__fig.add_subplot(num_rows, num_cols, ind))
                self.__getattribute__(key).set_title(key)
                self.__getattribute__(key).set_ylim([GENERIC_PARAMS[key][0] * 0.8, GENERIC_PARAMS[key][1] * 1.2])
                ind += 1
            self.__fitting = self.__fig.add_subplot(num_rows, num_cols, ind)
            self.__fitting.set_title("Individuals fitting")
            self.__fitting.set_ylim(
                [(get_population_size() * 0.9) - get_population_size(), get_population_size() * 1.1])
            self.__data = self.__fig.add_subplot(num_rows, num_cols, ind + 1)

        plt.xlabel("Iterations")
        plt.tight_layout()
        plt.gcf().subplots_adjust(bottom=0.08, right=0.9, left=0.1, top=0.9)

    def add_limits(self, environment_data):
        """
        This method is used to add some horizontal axis to the plots to understand better if the results
        make sens.
        :param environment_data: the current parameters against which the individuals are being tested
        :type environment_data: dict
        """
        if not is_generic():
            temp_threshold = 0.05 + (abs(environment_data["temperature"] - 20) * 0.01)
            self.__ax1.axhline(y=environment_data["predators_speed"], c="red", linewidth=0.5, zorder=0)
            self.__ax1.axhline(y=environment_data["food_animals_speed"], c="blue", linewidth=0.5, zorder=0)
            self.__ax2.axhline(y=environment_data["food_animals_strength"], c="blue", linewidth=0.5, zorder=0)
            self.__ax3.axhline(y=temp_threshold, c="blue", linewidth=0.5, zorder=0)
            self.__ax4.axhline(y=environment_data["tree_height"], c="blue", linewidth=0.5, zorder=0)
            environment_params = "\n".join([f"{key}: {value}" for key, value in environment_data.items()])
            self.__ax6.text(0.2, 0.5, environment_params, horizontalalignment="left", verticalalignment="center",
                            size=15)
            self.__ax6.text(0.2, 0.1, f"max_iterations: {max_iterations}", horizontalalignment="left",
                            verticalalignment="center", size=15)
            self.__ax6.axis("off")
        else:
            for key in environment_data.keys():
                self.__getattribute__(key).axhline(y=environment_data[key], c="red", linewidth=0.5, zorder=0)
            environment_params = "\n".join([f"{key}: {value}" for key, value in environment_data.items()])
            self.__data.text(0.2, 0.5, environment_params, horizontalalignment="left", verticalalignment="center",
                             size=15)
            self.__data.axis("off")

    def add_data(self, results, iteration):
        """
        This method adds the points to plot for the current iteration
        :param results: object containing the iteration average results
        :type results: dict
        :param iteration: current iteration
        :type iteration: int
        """
        if not is_generic():
            self.__ax1.scatter(iteration, results["speed"], color="r", s=3)
            self.__ax2.scatter(iteration, results["strength"], color="g", s=3)
            self.__ax3.scatter(iteration, results["skin"], color="b", s=3)
            self.__ax4.scatter(iteration, results["total_reach"], color="c", s=3)
            self.__ax5.scatter(iteration, results["fitting"], color="k", s=3)
        else:
            for key, val in results.items():
                if key not in ["value", "age", "_id"]:
                    self.__getattribute__(key).scatter(iteration, results[key], color="r", s=3)
            self.__fitting.scatter(iteration, results["fitting"], color="k", s=3)

    def save_results(self, plot_name):
        """
        This method creates the resulting environment plot
        :param plot_name: name of the plot to save
        :type plot_name: str
        """
        self.__fig.suptitle(plot_name, fontsize=20)
        plt.savefig(f"output/{plot_name}.png", transparent=False)
        logging.info(f"Results saved in the following file: output/{plot_name}.png")
