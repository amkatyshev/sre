from ufal.udpipe import Model, Pipeline, ProcessingError
from conllu import parse_tree
from SRE import Model as SREM
import os

MODULE_DIR = os.path.dirname(__file__)


class SRE(object):
    def __init__(self, udmodel=MODULE_DIR+'/russian.udpipe', srmodel=MODULE_DIR+'/ruwiki/wiki.model', encoding='utf8'):
        self.__udmodel__ = Model.load(udmodel)
        self.__pipeline__ = Pipeline(self.__udmodel__, 'horizontal', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')
        self.__log__ = open('log.txt', 'w', encoding=encoding)
        self.__srem__ = SREM(srmodel)

    def __evalTreeSentence__(self, sentenceRoot, indexSentence):
        logstr = '[sentence ' + str(indexSentence) + '] '
        upt_root = sentenceRoot.token['upostag']
        # если главная часть - существительное
        if upt_root == 'NOUN':
            try:
                # главная часть - существительное nsubj
                subjs = [_ for _ in sentenceRoot.children if
                         _.token['deprel'] == 'nsubj' and _.token['upostag'] == 'NOUN']
                if len(subjs) > 0:
                    # ... вместе с другими перечислениями
                    subjs.extend([_ for _ in subjs[0].children if
                                  _.token['deprel'] == 'conj' and subjs[0].token['upostag'] == _.token[
                                      'upostag']])
                # ... добавляем перечисления к корню
                rootsubjs = [sentenceRoot] + [_ for _ in sentenceRoot.children if
                                               _.token['deprel'] == 'conj' and _.token['upostag'] == 'NOUN']

                # добавляем зависимости от главных существительных в виде существительных в родительном падеже
                for s in subjs:
                    for rs in rootsubjs:
                        smods = [_ for _ in s.children if
                                 _.token['deprel'] == 'nmod' and _.token['upostag'] == 'NOUN' and
                                 _.token['feats']['Case'] == 'Gen']
                        slemma = s.token['lemma']
                        if (len(smods) > 0):
                            slemma += ' ' + smods[0].token['form']
                        rsmods = [_ for _ in rs.children if
                                  _.token['deprel'] == 'nmod' and _.token['upostag'] == 'NOUN' and
                                  _.token['feats']['Case'] == 'Gen']
                        rslemma = rs.token['lemma']
                        if (len(rsmods) > 0):
                            rslemma += ' ' + rsmods[0].token['form']
                        self.__log__.write(logstr + ' IS-A: ' + slemma + '<->' + rslemma + '\n')
            except Exception as e:
                self.__log__.write(logstr + ' error [' + str(e) + ']\n')
        # если главная часть - глагол "являться" или похожий на него
        elif upt_root == 'VERB' and sentenceRoot.token['lemma'] in self.__srem__.getSimilarWords('являться', 5):
            try:
                subjs = [_ for _ in sentenceRoot.children if
                         _.token['deprel'] == 'nsubj' and _.token['upostag'] == 'NOUN']
                if len(subjs) > 0:
                    subjs.extend([_ for _ in subjs[0].children if
                                  _.token['deprel'] == 'conj' and subjs[0].token['upostag'] == _.token[
                                      'upostag']])
                obls = [_ for _ in sentenceRoot.children if _.token['deprel'] == 'obl']
                if len(obls) > 0:
                    obls.extend([_ for _ in obls[0].children if
                                 _.token['deprel'] == 'conj' and obls[0].token['upostag'] == _.token[
                                     'upostag']])
                for s in subjs:
                    for o in obls:
                        self.__log__.write(logstr + ' IS-A: ' + s.token['lemma'] + '<->' + o.token['lemma'] + '\n')
            except Exception as e:
                self.__log__.write(logstr + ' error [' + str(e) + ']\n')

    def analyze(self, filename, encoding='utf8'):
        error = ProcessingError()
        with open(filename, 'r', encoding=encoding) as file:
            for index, line in enumerate(file, start=1):
                processed_conllu = self.__pipeline__.process(line, error)
                sentence_root = parse_tree(processed_conllu)[0]
                self.__evalTreeSentence__(sentence_root, index)



