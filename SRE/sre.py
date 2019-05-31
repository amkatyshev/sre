from ufal.udpipe import Model, Pipeline, ProcessingError
from conllu import parse_tree
from SRE.IOUtils import Output
from .TemplateParser import *
from SRE import WordModel
import os

MODULE_DIR = os.path.dirname(__file__)


class SRE(object):
    def __init__(self, wordModel=MODULE_DIR+'/ruwiki/wiki.model', output='result.txt'):
        self.__udmodel__ = Model.load(MODULE_DIR+'/rupipe/russian.udpipe')
        self.__pipeline__ = Pipeline(
            self.__udmodel__,
            'horizontal',
            Pipeline.DEFAULT,
            Pipeline.DEFAULT,
            'conllu')
        self.__srem__ = WordModel(wordModel)
        self.__out__ = Output(output)

    def __evalTreeSentence__(self, sentenceRoot):
        result = []
        templateParsers = [_class.__name__ for _class in AbstractTemplateParser.__subclasses__()]
        for className in templateParsers:
            _class = globals()[className]
            templateParser = _class(self.__srem__)
            parseSentenceResult = templateParser.parse(sentenceRoot)
            result += parseSentenceResult
        return result

    def analyze(self, filename, encoding='utf8'):
        error = ProcessingError()
        result = []
        with open(filename, 'r', encoding=encoding) as file:
            self.__out__.out('Analyzing file ' + filename + ':')
            for index, line in enumerate(file, start=1):
                processed_conllu = self.__pipeline__.process(line, error)
                sentence_root = parse_tree(processed_conllu)[0]
                result += self.__evalTreeSentence__(sentence_root)
        self.__out__.out(result)




