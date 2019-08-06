import sys

from src.tools.database.settings import MESSAGES


class DataWrapper:
    def __init__(self, db=None, params=None, environment=None):
        if db:
            if db.lower() == 'mongodb':
                from src.tools.database.mongodb_wrapper import MongodbDbWrapper
                self.db = True
                self.my_data = MongodbDbWrapper(params)
            elif db.lower() == 'mysql':
                from src.tools.database.mysql_wrapper import MysqlDbWrapper
                self.db = True
                self.my_data = MysqlDbWrapper(params, environment)
            else:
                print(MESSAGES["WRONG_DATABASE"])
                sys.exit()
        else:
            self.db = False
            self.my_data = {}

    def __setitem__(self, key, value):
        if not self.db and key not in self.my_data:
            self.my_data[key] = value
        self.my_data.__setitem__(key, value)

    def __getitem__(self, item):
        if not self.db and item not in self.my_data:
            self.my_data[item] = []
        return self.my_data[item]

    def __delitem__(self, key):
        self.my_data.__delitem__(key)
