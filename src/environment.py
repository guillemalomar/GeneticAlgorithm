class Environment:
    def __init__(self, name, data):
        self.__name = name
        self.__data = data

    @property
    def data(self):
        return self.__data

    @property
    def name(self):
        return self.__name
