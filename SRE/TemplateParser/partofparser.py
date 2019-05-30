from SRE.TemplateParser import AbstractTemplateParser
from SRE.filewriter import FileWriter


class PartOfParser(AbstractTemplateParser):
    def parse(self, sentence):
        if sentence.token['lemma'] in self.__wordModel__.getSimilarWords(['часть'], {'NOUN', 'inan', 'sing', 'nomn'}, 10):
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
            for s in concept1:
                fullConcept1 = s.token['lemma']
                fullConcept1Mod = [_ for _ in s.children if _.token['deprel'] == 'nmod']
                if len(fullConcept1Mod) > 0:
                    fullConcept1 += ' ' + fullConcept1Mod[0].token['form']
                for n in concept2:
                    fullConcept2 = n.token['lemma']
                    fullConcept2Mod = [_ for _ in n.children if _.token['deprel'] == 'nmod']
                    if len(fullConcept2Mod) > 0:
                        fullConcept2 += ' ' + fullConcept2Mod[0].token['form']
                    FileWriter.toFile('PART-OF: ' + fullConcept1 + '<->' + fullConcept2, 'log.txt')
