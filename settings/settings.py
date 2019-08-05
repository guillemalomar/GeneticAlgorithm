initial_population_size = 1000
max_iterations = 100
mutation_factor = 0.05
elitism = True

MESSAGES = {
    "CANCELLED_EXECUTION": "Execution cancelled manually",
    "POP_STAGE": "*** Population stage ***",
    "ITERATION_STAGE": "*** Iteration stage ***",
    "CLOSING_STAGE": "*** Closing stage ***",
    "MULTIPLE_AND_NAME": "The multiple flag has been activated, but a name for a single execution has been given. \n "
                         "Check your input parameters",
    "MULTIPLE_AND_PARAM": "The multiple flag has been activated, but single parameters have been specified. \n"
                          "Check your input parameters",
    "INCORR_PARAM_FORMAT": "The format of the parameters is incorrect.",
    "INCORR_PARAM_NUMBER": "The amount of parameters is incorrect.",
    "ABOUT_MESSAGE": 30 * "#" + " Genetic Algorithm " + 31 * "#" + '\n' +
                     "# This project is an example of the most classic Genetic Algorithm problem.    #\n" +
                     "# The default mode will obtain 1 or more environments, will create a set of    #\n" +
                     "# individuals with random parameters values within a specified range, and will #\n" +
                     "# show how these parameters change when facing the individuals against the     #\n" +
                     "# environments over many iterations.                                           #\n" +
                     80 * "#"
}
