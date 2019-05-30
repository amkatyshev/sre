from SRE.TemplateParser import AbstractTemplateParser
from SRE.filewriter import FileWriter


class IsAParser(AbstractTemplateParser):
    def parse(self, sentence):
        # если главная часть - существительное
        if sentence.token['upostag'] == 'NOUN' and sentence.token['lemma'] != 'часть':
            try:
                # главная часть - существительное nsubj
                concept1 = self.__getChildrenByToken__(sentence, {'deprel': 'nsubj'})
                if concept1:
                    # ... вместе с другими перечислениями
                    concept1.extend(self.__getChildrenByToken__(concept1[0], {'deprel': 'conj'}))
                # ... добавляем перечисления к корню
                concept2 = [sentence] + self.__getChildrenByToken__(sentence, {'deprel': 'conj'})

                # добавляем зависимости от главных существительных в виде существительных в родительном падеже
                for c1 in concept1:
                    fullConcept1 = self.__getFullConcept__(c1)
                    for c2 in concept2:
                        fullConcept2 = self.__getFullConcept__(c2)
                        FileWriter.toFile('IS-A: ' + fullConcept1 + '<->' + fullConcept2, 'log.txt')
            except Exception as e:
                FileWriter.toFile('error [' + str(e) + ']', 'log.txt')
        # если главная часть - глагол "являться" или похожий на него
        elif sentence.token['upostag'] == 'VERB' and \
                sentence.token['lemma'] in self.__wordModel__.getSimilarWords(['являться', 'называться'], {'INFN'}, 10) and \
                not self.__getChildrenByToken__(sentence, {'lemma': 'часть'}):
            try:
                # главная часть - существительное nsubj
                concept1 = self.__getChildrenByToken__(sentence, {'deprel': 'nsubj'})
                if concept1:
                    # ... вместе с другими перечислениями
                    concept1.extend(self.__getChildrenByToken__(concept1[0], {'deprel': 'conj'}))

                concept2 = self.__getChildrenByToken__(sentence, {'deprel': 'obl'})
                if concept2:
                    concept2.extend(self.__getChildrenByToken__(concept1[0], {'deprel': 'conj'}))

                for c1 in concept1:
                    fullConcept1 = self.__getFullConcept__(c1)
                    for c2 in concept2:
                        fullConcept2 = self.__getFullConcept__(c2)
                        FileWriter.toFile('IS-A: ' + fullConcept1 + '<->' + fullConcept2, 'log.txt')
            except Exception as e:
                FileWriter.toFile('error [' + str(e) + ']', 'log.txt')
