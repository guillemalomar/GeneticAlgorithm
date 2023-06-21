import sys
from src.tools.plot import PlotWrapper


my_plot = PlotWrapper()
my_data_wrapper = {}


def set_db(to_activate=None, environment=None):
    from src.tools.database.data_wrapper import DataWrapper
    global my_data_wrapper
    if to_activate:
        if to_activate.lower() == "mongodb":
            from creds import MONGODB_PARAMS
            my_data_wrapper = DataWrapper(db=to_activate, params=MONGODB_PARAMS)
        elif to_activate.lower() == "mysql":
            from creds import MYSQL_PARAMS
            my_data_wrapper = DataWrapper(db=to_activate, params=MYSQL_PARAMS, environment=environment)
        elif to_activate.lower() == "no db":
            my_data_wrapper = DataWrapper()
        else:
            print("Choose one of the available DB")
            sys.exit()
    else:
        my_data_wrapper = DataWrapper()


def check_db():
    if my_data_wrapper:
        return True
    return False


def return_db():
    return my_data_wrapper
