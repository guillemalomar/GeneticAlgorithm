import sys

from src.tools.mongo_wrapper import MongoWrapper


class DataWrapper:
    def __init__(self, db=None):
        if db.lower() == 'mongodb':
            self.my_data = MongoWrapper()
        elif db.lower() == 'mysql':
            print("Use of MySQL is not available (yet :P)")
            sys.exit()
        else:
            self.my_data = {}
            self.current_dict = ''

    def __setitem__(self, key, value):
        if type(self.my_data) is dict and key not in self.my_data:
            self.current_dict = key
            self.my_data[key] = value
        self.my_data.__setitem__(key, value)

    def __getitem__(self, item):
        if type(self.my_data) is dict and item not in self.my_data:
            self.my_data[item] = []
        return self.my_data[item]

    def __delitem__(self, key):
        self.my_data.__delitem__(key)
