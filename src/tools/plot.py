import logging
import matplotlib.pyplot as plt

from settings.settings import INDIVIDUALS_PARAMS as limits, initial_population_size


class PlotWrapper:
    def __init__(self):
        self.fig = plt.figure(figsize=(12, 9))
        self.fig = self.fig
        self.ax1 = self.fig.add_subplot(3, 2, 1)
        self.ax1.set_title('Average Speed')
        self.ax1.set_ylim([limits['speed'][0]*0.8, limits['speed'][1]*1.2])
        self.ax2 = self.fig.add_subplot(3, 2, 2)
        self.ax2.set_title('Average Strength')
        self.ax2.set_ylim([limits['strength'][0]*0.8, limits['strength'][1]*1.2])
        self.ax3 = self.fig.add_subplot(3, 2, 3)
        self.ax3.set_title('Average Skin thickness')
        self.ax3.set_ylim([limits['skin_thickness'][0]*0.8, limits['skin_thickness'][1]*1.2])
        self.ax4 = self.fig.add_subplot(3, 2, 4)
        self.ax4.set_title('Average Total Reach')
        self.ax4.set_ylim([1*0.8, 2.5*1.2])
        self.ax5 = self.fig.add_subplot(3, 2, 5)
        self.ax5.set_title('Individuals fitting')
        self.ax5.set_ylim([(initial_population_size * 0.9) - initial_population_size, initial_population_size*1.1])
        self.ax6 = self.fig.add_subplot(3, 2, 6)
        plt.xlabel("Iterations")
        plt.tight_layout()
        plt.gcf().subplots_adjust(bottom=0.08, right=0.9, left=0.1, top=0.9)

    def add_limits(self, environment):
        self.ax1.axhline(y=environment['predators_speed'], c="red", linewidth=0.5, zorder=0)
        self.ax1.axhline(y=environment['food_animals_speed'], c="blue", linewidth=0.5, zorder=0)
        self.ax2.axhline(y=environment['food_animals_strength'], c="blue", linewidth=0.5, zorder=0)
        self.ax4.axhline(y=environment['tree_height'], c="blue", linewidth=0.5, zorder=0)

        environment_params = '\n'.join(['{}: {}'.format(key, value) for key, value in environment.items()])
        self.ax6.text(0.2, 0.5, environment_params, horizontalalignment='left', verticalalignment='center', size=15)
        self.ax6.axis('off')

    def add_data(self, results, iteration):
        self.ax1.scatter(iteration, results['avg_speed'], color='r', s=3)
        self.ax2.scatter(iteration, results['avg_strength'], color='g', s=3)
        self.ax3.scatter(iteration, results['avg_skin'], color='b', s=3)
        self.ax4.scatter(iteration, results['total_reach'], color='c', s=3)
        self.ax5.scatter(iteration, results['fitting'], color='k', s=3)

    def save_results(self, plot_name):
        self.fig.suptitle(plot_name, fontsize=20)
        plt.savefig("output/{}.png".format(plot_name), transparent=False)
        logging.info("Results saved in the following file: output/{}.png".format(plot_name))
