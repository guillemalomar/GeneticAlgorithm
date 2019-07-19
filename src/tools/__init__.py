from src.tools.plot import PlotWrapper


my_plot = PlotWrapper()
my_mongo_wrapper = None


def set_db(activate):
    from src.tools.mongodb_wrapper import MongoDBWrapper
    global my_mongo_wrapper
    if activate:
        my_mongo_wrapper = MongoDBWrapper()
    else:
        my_mongo_wrapper = False


def check_and_return_db():
    return my_mongo_wrapper
