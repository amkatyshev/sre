from SRE.TemplateParser import AbstractTemplateParser


class IsAParser(AbstractTemplateParser):
    @staticmethod
    def getTemplateName():
        return 'IS-A'

    def parse(self, sentence):
        result = []
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
                        if self.__wordModel__.isTrueConcept(self.__themes__, c1.token['form']) or \
                            self.__wordModel__.isTrueConcept(self.__themes__, c2.token['form']):
                            result.append((fullConcept1, fullConcept2))
            except Exception as e:
                raise Exception('Error with parsing IS-A template: ' + str(e))
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
                        if self.__wordModel__.isTrueConcept(self.__themes__, c1.token['form']) or \
                            self.__wordModel__.isTrueConcept(self.__themes__, c2.token['form']):
                            result.append((fullConcept1, fullConcept2))
            except Exception as e:
                raise Exception('Error with parsing IS-A template: ' + str(e))

        return result
