from SRE.TemplateParser import AbstractTemplateParser
from SRE.filewriter import FileWriter


class IsAParser(AbstractTemplateParser):
    def parse(self, sentence):
        upt_root = sentence.token['upostag']
        # если главная часть - существительное
        if upt_root == 'NOUN' and sentence.token['lemma'] != 'часть':
            try:
                # главная часть - существительное nsubj
                subjs = [_ for _ in sentence.children if
                         _.token['deprel'] == 'nsubj' and _.token['upostag'] == 'NOUN']
                if len(subjs) > 0:
                    # ... вместе с другими перечислениями
                    subjs.extend([_ for _ in subjs[0].children if
                                  _.token['deprel'] == 'conj' and subjs[0].token['upostag'] == _.token[
                                      'upostag']])
                # ... добавляем перечисления к корню
                rootsubjs = [sentence] + [_ for _ in sentence.children if
                                              _.token['deprel'] == 'conj' and _.token['upostag'] == 'NOUN']

                # добавляем зависимости от главных существительных в виде существительных в родительном падеже
                for s in subjs:
                    for rs in rootsubjs:
                        smods = [_ for _ in s.children if
                                 _.token['deprel'] == 'nmod' and _.token['upostag'] == 'NOUN' and
                                 _.token['feats']['Case'] == 'Gen']
                        slemma = s.token['lemma']
                        if len(smods) > 0:
                            slemma += ' ' + smods[0].token['form']
                        rsmods = [_ for _ in rs.children if
                                  _.token['deprel'] == 'nmod' and _.token['upostag'] == 'NOUN' and
                                  _.token['feats']['Case'] == 'Gen']
                        rslemma = rs.token['lemma']
                        if len(rsmods) > 0:
                            rslemma += ' ' + rsmods[0].token['form']
                        FileWriter.toFile('IS-A: ' + slemma + '<->' + rslemma, 'log.txt')
            except Exception as e:
                FileWriter.toFile('error [' + str(e) + ']', 'log.txt')
        # если главная часть - глагол "являться" или похожий на него
        elif upt_root == 'VERB' and sentence.token['lemma'] in self.__wordModel__.getSimilarWords(
                ['являться', 'называться'], {'INFN'}, 10):
            try:
                subjs = [_ for _ in sentence.children if
                         _.token['deprel'] == 'nsubj' and _.token['upostag'] == 'NOUN']
                if len(subjs) > 0:
                    subjs.extend([_ for _ in subjs[0].children if
                                  _.token['deprel'] == 'conj' and subjs[0].token['upostag'] == _.token[
                                      'upostag']])
                obls = [_ for _ in sentence.children if _.token['deprel'] == 'obl']
                if len(obls) > 0:
                    obls.extend([_ for _ in obls[0].children if
                                 _.token['deprel'] == 'conj' and obls[0].token['upostag'] == _.token[
                                     'upostag']])
                for s in subjs:
                    for o in obls:
                        FileWriter.toFile('IS-A: ' + s.token['lemma'] + '<->' + o.token['lemma'], 'log.txt')
            except Exception as e:
                FileWriter.toFile('error [' + str(e) + ']', 'log.txt')
