import matplotlib.pyplot as plt


class PlotWrapper():
    def __init__(self):
        fig = plt.figure(figsize=(20, 10))
        self.fig = fig
        self.ax1 = self.fig.add_subplot(4, 2, 1)
        self.ax1.set_title('Average Speed')
        self.ax2 = self.fig.add_subplot(4, 2, 2)
        self.ax2.set_title('Average Strength')
        self.ax3 = self.fig.add_subplot(4, 2, 3)
        self.ax3.set_title('Average Height')
        self.ax4 = self.fig.add_subplot(4, 2, 4)
        self.ax4.set_title('Average arm length')
        self.ax5 = self.fig.add_subplot(4, 2, 5)
        self.ax5.set_title('Average Skin thickness')
        self.ax6 = self.fig.add_subplot(4, 2, 6)
        self.ax6.set_title('Average Jump')
        self.ax7 = self.fig.add_subplot(4, 2, 7)
        self.ax7.set_title('Average Total Reach')
        self.ax8 = self.fig.add_subplot(4, 2, 8)
        self.ax8.set_title('Individuals not fitting')
        plt.xlabel("Iterations")
        plt.tight_layout()

    def add_data(self, results, iteration):
        self.ax1.scatter(iteration, results['avg_speed'])
        self.ax2.scatter(iteration, results['avg_strength'])
        self.ax3.scatter(iteration, results['avg_height'])
        self.ax4.scatter(iteration, results['avg_arm'])
        self.ax5.scatter(iteration, results['avg_skin'])
        self.ax6.scatter(iteration, results['avg_jump'])
        self.ax7.scatter(iteration, results['total_reach'])
        self.ax8.scatter(iteration, results['not_fitting'])

    @staticmethod
    def save_results(iteration):
        plt.savefig("../output/{}.png".format(iteration), transparent=False)
