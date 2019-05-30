from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractTemplateParser:
    def __init__(self, wordModel):
        __metaclass__ = ABCMeta
        self.__wordModel__ = wordModel

    @abstractmethod
    def parse(self, sentence):
        """Разбор предложения для данного шаблона"""
