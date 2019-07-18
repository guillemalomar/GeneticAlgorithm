import matplotlib.pyplot as plt

from settings import INDIVIDUALS_PARAMS as limits, initial_population_size


class PlotWrapper():
    def __init__(self):
        self.fig = plt.figure(figsize=(12, 9))
        self.fig = self.fig
        self.ax1 = self.fig.add_subplot(4, 2, 1)
        self.ax1.set_title('Average Speed')
        self.ax1.set_ylim([limits['speed'][0]*0.8, limits['speed'][1]*1.2])
        self.ax2 = self.fig.add_subplot(4, 2, 2)
        self.ax2.set_title('Average Strength')
        self.ax2.set_ylim([limits['strength'][0]*0.8, limits['strength'][1]*1.2])
        self.ax3 = self.fig.add_subplot(4, 2, 3)
        self.ax3.set_title('Average Height')
        self.ax3.set_ylim([limits['height'][0]*0.8, limits['height'][1]*1.2])
        self.ax4 = self.fig.add_subplot(4, 2, 4)
        self.ax4.set_title('Average arm length')
        self.ax4.set_ylim([limits['arm_length'][0]*0.8, limits['arm_length'][1]*1.2])
        self.ax5 = self.fig.add_subplot(4, 2, 5)
        self.ax5.set_title('Average Skin thickness')
        self.ax5.set_ylim([limits['skin_thickness'][0]*0.8, limits['skin_thickness'][1]*1.2])
        self.ax6 = self.fig.add_subplot(4, 2, 6)
        self.ax6.set_title('Average Jump')
        self.ax6.set_ylim([limits['jump'][0]*0.8, limits['jump'][1]*1.2])
        self.ax7 = self.fig.add_subplot(4, 2, 7)
        self.ax7.set_title('Average Total Reach')
        self.ax7.set_ylim([1, 2.5*1.2])
        self.ax8 = self.fig.add_subplot(4, 2, 8)
        self.ax8.set_title('Individuals not fitting')
        self.ax8.set_ylim([0, initial_population_size])
        plt.xlabel("Iterations")
        plt.tight_layout()
        plt.gcf().subplots_adjust(bottom=0.1, right=0.9, left=0.1, top=0.9)

    def add_limits(self, environment):
        self.ax1.axhline(y=environment['predators_speed'], c="red", linewidth=0.5, zorder=0)
        self.ax1.axhline(y=environment['food_animals_speed'], c="blue", linewidth=0.5, zorder=0)
        self.ax2.axhline(y=environment['food_animals_strength'], c="blue", linewidth=0.5, zorder=0)
        self.ax7.axhline(y=environment['fruit_tree_height'], c="blue", linewidth=0.5, zorder=0)

    def add_data(self, results, iteration):
        self.ax1.scatter(iteration, results['avg_speed'])
        self.ax2.scatter(iteration, results['avg_strength'])
        self.ax3.scatter(iteration, results['avg_height'])
        self.ax4.scatter(iteration, results['avg_arm'])
        self.ax5.scatter(iteration, results['avg_skin'])
        self.ax6.scatter(iteration, results['avg_jump'])
        self.ax7.scatter(iteration, results['total_reach'])
        self.ax8.scatter(iteration, results['not_fitting'])

    def save_results(self, plot_name):
        self.fig.suptitle(plot_name, fontsize=20)
        plt.savefig("../output/{}.png".format(plot_name), transparent=False)
