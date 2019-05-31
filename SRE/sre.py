from ufal.udpipe import Model, Pipeline, ProcessingError
from conllu import parse_tree
from SRE.IOUtils import Output
from .TemplateParser import *
from SRE import WordModel
from SRE import Result
import os

MODULE_DIR = os.path.dirname(__file__)


class SRE(object):
    def __init__(self, wordModel=MODULE_DIR+'/ruwiki/wiki.model'):
        self.__udmodel__ = Model.load(MODULE_DIR+'/rupipe/russian.udpipe')
        self.__pipeline__ = Pipeline(
            self.__udmodel__,
            'horizontal',
            Pipeline.DEFAULT,
            Pipeline.DEFAULT,
            'conllu')
        self.__srem__ = WordModel(wordModel)
        self.__result__ = Result()

    def __evalTreeSentence__(self, sentenceRoot):
        templateParsers = [_class.__name__ for _class in AbstractTemplateParser.__subclasses__()]
        for className in templateParsers:
            _class = globals()[className]
            templateParser = _class(self.__srem__)
            templateValue = templateParser.getTemplate()
            parseSentenceResult = templateParser.parse(sentenceRoot)
            self.__result__.add({templateValue: parseSentenceResult})

    def analyze(self, filename, encoding='utf8'):
        error = ProcessingError()
        with open(filename, 'r', encoding=encoding) as file:
            for index, line in enumerate(file, start=1):
                processed_conllu = self.__pipeline__.process(line, error)
                sentence_root = parse_tree(processed_conllu)[0]
                self.__evalTreeSentence__(sentence_root)

    def getFullResult(self, output):
        out = Output(output)
        out.out(self.__result__.getData())



