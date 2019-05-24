from ufal.udpipe import Model, Pipeline, ProcessingError
from conllu import parse_tree


class SRE(object):
    def __init__(self, udmodel):
        self.__udmodel__ = Model.load(udmodel)
        self.__pipeline__ = Pipeline(self.__udmodel__, 'horizontal', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')

    def analyze(self, filename, encoding='utf8'):
        error = ProcessingError()
        log = open('log.txt', 'w', encoding=encoding)
        with open(filename, 'r', encoding=encoding) as file:
            for index, line in enumerate(file, start=1):
                processed_conllu = self.__pipeline__.process(line, error)
                sentence_root = parse_tree(processed_conllu)[0]
                logstr = '[sentence ' + str(index) + '] '
                # is-a связь - корень NOUN
                upt_root = sentence_root.token['upostag']
                if upt_root == 'NOUN':
                    try:
                        subjs = [_ for _ in sentence_root.children if
                                 _.token['deprel'] == 'nsubj' and _.token['upostag'] == 'NOUN']
                        if len(subjs) > 0:
                            subjs.extend([_ for _ in subjs[0].children if
                                          _.token['deprel'] == 'conj' and subjs[0].token['upostag'] == _.token[
                                              'upostag']])
                        rootsubjs = [sentence_root] + [_ for _ in sentence_root.children if
                                                       _.token['deprel'] == 'conj' and _.token['upostag'] == 'NOUN']
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
                                log.write(logstr + ' IS-A: ' + slemma + '<->' + rslemma + '\n')
                    except Exception as e:
                        log.write(logstr + ' error [' + str(e) + ']\n')
                elif upt_root == 'VERB' and sentence_root.token['lemma'] == 'являться':
                    try:
                        subjs = [_ for _ in sentence_root.children if
                                 _.token['deprel'] == 'nsubj' and _.token['upostag'] == 'NOUN']
                        if len(subjs) > 0:
                            subjs.extend([_ for _ in subjs[0].children if
                                          _.token['deprel'] == 'conj' and subjs[0].token['upostag'] == _.token[
                                              'upostag']])
                        obls = [_ for _ in sentence_root.children if _.token['deprel'] == 'obl']
                        if len(obls) > 0:
                            obls.extend([_ for _ in obls[0].children if
                                         _.token['deprel'] == 'conj' and obls[0].token['upostag'] == _.token[
                                             'upostag']])
                        for s in subjs:
                            for o in obls:
                                log.write(logstr + ' IS-A: ' + s.token['lemma'] + '<->' + o.token['lemma'] + '\n')
                    except Exception as e:
                        log.write(logstr + ' error [' + str(e) + ']\n')
        log.close()
