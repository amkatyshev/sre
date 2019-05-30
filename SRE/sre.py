from ufal.udpipe import Model, Pipeline, ProcessingError
from conllu import parse_tree
from .filewriter import FileWriter
from .TemplateParser import *
from SRE import WordModel
import os

MODULE_DIR = os.path.dirname(__file__)


class SRE(object):
    def __init__(self, udModel=MODULE_DIR+'/russian.udpipe', wordModel=MODULE_DIR+'/ruwiki/wiki.model', encoding='utf8'):
        self.__udmodel__ = Model.load(udModel)
        self.__pipeline__ = Pipeline(self.__udmodel__, 'horizontal', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')
        self.__srem__ = WordModel(wordModel)

    def __evalTreeSentence__(self, sentenceRoot, indexSentence):
        print('Parse sentence ' + str(indexSentence) + '... ', end='')
        # FileWriter.toFile('[sentence ' + str(indexSentence) + '] ', 'log.txt', ' ')
        templateParser = IsAParser(self.__srem__)
        templateParser.parse(sentenceRoot)
        print('[OK]', end='\n')

    def analyze(self, filename, encoding='utf8'):
        error = ProcessingError()
        with open(filename, 'r', encoding=encoding) as file:
            for index, line in enumerate(file, start=1):
                processed_conllu = self.__pipeline__.process(line, error)
                sentence_root = parse_tree(processed_conllu)[0]
                self.__evalTreeSentence__(sentence_root, index)



