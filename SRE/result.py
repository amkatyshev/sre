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

    def getDataByType(self, type, concept=None):
        result = {}
        if type in self.__data__:
            if not concept:
                result = {type: self.__data__[type]}
            else:
                result.setdefault(type, [])
                for tuple in self.__data__[type]:
                    if concept in tuple:
                        result.update({type: result.get(type) + [tuple]})
            return result
