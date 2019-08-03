import logging


def show_about():
    print(30 * "#" + " Genetic Algorithm " + 31 * "#")
    print("# This project is an example of the most classic Genetic Algorithm problem.    #\n" +
          "# The default mode will obtain 1 or more environments, will create a set of    #\n" +
          "# individuals with random parameters values within a specified range, and will #\n" +
          "# show how these parameters change when facing the individuals against the     #\n" +
          "# environments over many iterations.                                           #")
    print(80 * "#")


def execution_message(environment):
    msg = 20 * "#" + " NEW EXECUTION " + 20 * "#" + "\n" + \
          33*"#" + " Executing with the following parameters:\n" +\
          33*"#" + " Environment name: {}\n".format(environment.name) + 33*"#" + " -" +\
          "\n################################# -".join(
              ['{}: {}'.format(key, value) for key, value in environment.data.items()])
    print(msg)
    logging.info(msg)
