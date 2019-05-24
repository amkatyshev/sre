from ufal.udpipe import Model, Pipeline, ProcessingError
from conllu import parse_tree


class SRE(object):
    def __init__(self, udmodel):
        self.__udmodel__ = Model.load(udmodel)
        self.__pipeline__ = Pipeline(self.__udmodel__, 'horizontal', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')



