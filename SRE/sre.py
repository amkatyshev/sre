from ufal.udpipe import Model, Pipeline, ProcessingError
from conllu import parse_tree
from SRE.IOUtils import Output
from .TemplateParser import *
from SRE import WordModel
from SRE import Result
import os

MODULE_DIR = os.path.dirname(__file__)


class SRE(object):
    def __init__(self, udmodel, wordModel):
        self.__udmodel__ = Model.load(udmodel)
        if self.__udmodel__ is None:
            raise ValueError('Unknown UDPipe model')
        self.__pipeline__ = Pipeline(
            self.__udmodel__,
            'horizontal',
            Pipeline.DEFAULT,
            Pipeline.DEFAULT,
            'conllu')
        self.__uderror__ = ProcessingError()
        self.__srem__ = WordModel(wordModel)
        self.__result__ = Result()

    def __checkerThemes__(self, themes):
        if isinstance(themes, list):
            for theme in themes:
                if not isinstance(theme, str):
                    raise TypeError('Themes list must contain only str objects')
        else:
            raise TypeError('Themes must be list of str')

    def __evalTreeSentence__(self, themes, sentenceRoot):
        templateParsers = [_class.__name__ for _class in AbstractTemplateParser.__subclasses__()]
        for className in templateParsers:
            _class = globals()[className]
            templateParser = _class(themes, self.__srem__)
            templateValue = _class.getTemplateName()
            parseSentenceResult = templateParser.parse(sentenceRoot)
            self.__result__.add({templateValue: parseSentenceResult})
        conjRoots = [_ for _ in sentenceRoot.children if _.token['deprel'] == 'conj']
        if conjRoots:
            for conjRoot in conjRoots:
                self.__evalTreeSentence__(themes, conjRoot)

    def analyze(self, themes, filename, encoding='utf8'):
        self.__checkerThemes__(themes)
        print('Updating model with text... ', end='')
        self.__srem__.trainFile(filename, encoding=encoding)
        print('[OK]')
        print('Parsing sentences... ', end='')
        with open(filename, 'r', encoding=encoding) as file:
            for index, line in enumerate(file, start=1):
                processed_conllu = self.__pipeline__.process(line, self.__uderror__)
                if self.__uderror__.occurred():
                    raise RuntimeError('UDPipe error: ' + self.__uderror__.message)
                sentence_root = parse_tree(processed_conllu)[0]
                self.__evalTreeSentence__(themes, sentence_root)
        print('[OK]')

    def getFullResult(self, outputMode=Output.TO_FILE, filename='result.txt'):
        print('Getting full result... ')
        out = Output(outputMode, filename)
        out.out(self.__result__.getData())

    def getResultByType(self, type, concept=None, outputMode=Output.TO_FILE, filename='result.txt'):
        templateParsers = [_class.__name__ for _class in AbstractTemplateParser.__subclasses__()]
        availableTypes = [globals()[_].getTemplateName() for _ in templateParsers]
        if type in availableTypes:
            print('Getting result by type ' + type + '... ')
            out = Output(outputMode, filename)
            out.out(self.__result__.getDataByType(type, concept))
        else:
            raise AttributeError('Unknown semantic type. Available types: ' + ', '.join(availableTypes))



