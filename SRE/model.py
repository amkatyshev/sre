from gensim.models import Word2Vec, KeyedVectors
from pymorphy2 import MorphAnalyzer


class WordModel(object):
    def __init__(self, fileModel, isVector=False, binary=False):
        self.__morph__ = MorphAnalyzer()
        if isVector:
            model = KeyedVectors.load_word2vec_format(fileModel, binary=binary)
        else:
            model = Word2Vec.load(fileModel)
        self.__model__ = model
        self.__cache__ = []

    def __mostSimilar__(self, words, topn=10):
        return self.__model__.wv.most_similar(words, topn=topn)

    def __findWordInCache__(self, word):
        for wordCache in self.__cache__:
            if wordCache[0] == word:
                return wordCache
        return False

    def getModel(self):
        return self.__model__

    def getSimilarWords(self, words, count=10, grammems={'INFN'}):
        wordInCache = self.__findWordInCache__(words)
        if wordInCache == False:
            wordlist = self.__mostSimilar__(words, topn=count * 10)
            finalWords = []
            for wordInList in wordlist:
                if len(finalWords) < count:
                    word_parse = self.__morph__.parse(wordInList[0])[0]
                    inflect = word_parse.inflect(grammems)
                    if inflect.word not in finalWords:
                        finalWords.append(inflect.word)
            finalWords.extend(words)
            self.__cache__.append((words, finalWords))
            return finalWords
        else:
            return wordInCache[1]
