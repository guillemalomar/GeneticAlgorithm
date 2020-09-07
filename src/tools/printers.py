import logging

from settings.settings import MESSAGES


def show_about():
    print(MESSAGES["ABOUT_MESSAGE"])


def execution_message(environment):
    exec_message = 20 * "#" + " NEW EXECUTION " + 20 * "#" + "\n" + \
                   33*"#" + " Executing with the following parameters:\n" +\
                   33*"#" + f" Environment name: {environment.name}\n" + 33*"#" + " -" +\
                   "\n################################# -".join(
                       [f'{key}: {value}' for key, value in environment.data.items()])
    print(exec_message)
    logging.info(exec_message)
