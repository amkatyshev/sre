from SRE.TemplateParser import AbstractTemplateParser


class PartOfParser(AbstractTemplateParser):
    @staticmethod
    def getTemplateName():
        return 'PART-OF'

    def parse(self, sentence):
        result = []
        similarPartOfWords = self.__wordModel__.getSimilarWords(['часть'], {'NOUN', 'nomn'}, 10)
        if sentence.token['lemma'] in similarPartOfWords:
            # главная часть - существительное nsubj
            concept1 = [_ for _ in sentence.children if _.token['deprel'] == 'nsubj']
            if len(concept1) > 0:
                # ... вместе с другими перечислениями
                concept1.extend([_ for _ in concept1[0].children if _.token['deprel'] == 'conj'])

            # второй концепт
            concept2 = [_ for _ in sentence.children if _.token['deprel'] == 'nmod']
            if len(concept2) > 0:
                # ... вместе с другими перечислениями
                concept2.extend([_ for _ in concept2[0].children if _.token['deprel'] == 'conj'])
            for c1 in concept1:
                fullConcept1 = self.__getFullConcept__(c1)
                for c2 in concept2:
                    fullConcept2 = self.__getFullConcept__(c2)
                    if self.__wordModel__.isTrueConcept(self.__themes__, c1.token['form']) and \
                            self.__wordModel__.isTrueConcept(self.__themes__, c2.token['form']):
                        result.append((fullConcept1, fullConcept2))

        elif sentence.token['lemma'] in self.__wordModel__.getSimilarWords(['являться', 'называться'], {'INFN'}, 10) or \
                self.__getChildrenByToken__(sentence, {'lemma': 'часть'}):
            concept1 = []
            concept2 = []
            nsubj = self.__getChildrenByToken__(sentence, {'deprel': 'nsubj'})
            obl = self.__getChildrenByToken__(sentence, {'deprel': 'obl'})
            if nsubj and nsubj[0].token['lemma'] in similarPartOfWords:
                concept1 = self.__getChildrenByToken__(nsubj[0], {'deprel': 'nmod'})
                concept2 = obl
            elif obl and obl[0].token['lemma'] in similarPartOfWords:
                concept1 = nsubj
                concept2 = self.__getChildrenByToken__(obl[0], {'deprel': 'nmod'})

            if concept1:
                concept1.extend(self.__getChildrenByToken__(concept1[0], {'deprel': 'conj'}))
            if concept2:
                concept2.extend(self.__getChildrenByToken__(concept2[0], {'deprel': 'conj'}))

            for c1 in concept1:
                fullConcept1 = self.__getFullConcept__(c1)
                for c2 in concept2:
                    fullConcept2 = self.__getFullConcept__(c2)
                    if self.__wordModel__.isTrueConcept(self.__themes__, c1.token['form']) or \
                            self.__wordModel__.isTrueConcept(self.__themes__, c2.token['form']):
                        result.append((fullConcept1, fullConcept2))

        return result

