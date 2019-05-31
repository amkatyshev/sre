class Result(object):
    def __init__(self):
        self.__data__ = {}

    def add(self, data):
        for k, v in data.items():
            if k in self.__data__:
                self.__data__.update({k: self.__data__.get(k) + v})
            else:
                self.__data__.setdefault(k, v)

    def getData(self):
        return self.__data__
