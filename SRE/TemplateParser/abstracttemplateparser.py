from abc import ABCMeta, abstractmethod


class AbstractTemplateParser:
    def __init__(self, themes, wordModel):
        __metaclass__ = ABCMeta
        self.__wordModel__ = wordModel
        self.__themes__ = themes

    def __getChildrenByToken__(self, node, conditions={}):
        result = []
        conditionKeys = conditions.keys()
        for child in node.children:
            isCanAppend = True
            for key in conditionKeys:
                if child.token[key] != conditions[key]:
                    isCanAppend = False
                    break
            if isCanAppend:
                result.append(child)
        return result

    def __getFullConcept__(self, node):
        fullConcept = node.token['lemma']
        fullConceptMod = self.__getChildrenByToken__(node, {'deprel': 'nmod'})
        if fullConceptMod:
            fullConcept += ' (' + fullConceptMod[0].token['form'] + ')'
        return fullConcept

    @abstractmethod
    def parse(self, sentence):
        """Разбор предложения для данного шаблона"""

    @staticmethod
    @abstractmethod
    def getTemplateName():
        """Получение типа шаблона"""
