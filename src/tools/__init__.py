import logging

from src.tools.plot import PlotWrapper


my_plot = PlotWrapper()
my_mongo_wrapper = None


def set_db(to_activate):
    from src.tools.db_wrapper import DBWrapper
    global my_mongo_wrapper
    if to_activate:
        logging.debug("MongoDB will be used in this execution")
        my_mongo_wrapper = DBWrapper()
    else:
        my_mongo_wrapper = {}


def check_db():
    if my_mongo_wrapper:
        return True
    return False


def return_db():
    return my_mongo_wrapper
