from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractTemplateParser:
    def __init__(self, wordModel):
        __metaclass__ = ABCMeta
        self.__wordModel__ = wordModel

    def __getChildrenByToken__(self, node, conditions={}):
        result = []
        conditionKeys = conditions.keys()
        for child in node.children:
            isCanAppend = True
            for key in conditionKeys:
                if child.token[key] != conditions[key]:
                    isCanAppend = False
                    break
            if isCanAppend:
                result.append(child)
        return result

    @abstractmethod
    def parse(self, sentence):
        """Разбор предложения для данного шаблона"""
