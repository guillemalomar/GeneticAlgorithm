from src.tools.plot import PlotWrapper


my_plot = PlotWrapper()
my_data_wrapper = {}


def set_db(to_activate=None):
    from src.tools.data_wrapper import DataWrapper
    global my_data_wrapper
    if to_activate:
        my_data_wrapper = DataWrapper(to_activate)
    else:
        my_data_wrapper = DataWrapper()


def check_db():
    if my_data_wrapper:
        return True
    return False


def return_db():
    return my_data_wrapper
