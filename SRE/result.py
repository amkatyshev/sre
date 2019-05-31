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
            if concept is None:
                result = {type: self.__data__[type]}
            elif isinstance(concept, str):
                result.setdefault(type, [])
                for tuple in self.__data__[type]:
                    conceptsString = ' '.join(tuple)
                    if conceptsString.find(concept) > -1:
                        result.update({type: result.get(type) + [tuple]})
            else:
                raise AttributeError('Concept must be str type or None')
            return result
