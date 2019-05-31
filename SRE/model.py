from gensim.models import Word2Vec, KeyedVectors
from gensim.models.word2vec import LineSentence
from gensim.utils import keep_vocab_item
from pymorphy2 import MorphAnalyzer


class WordModel(object):
    def __init__(self, fileModel, isVector=False, binary=False):
        self.__morph__ = MorphAnalyzer()
        if isVector:
            model = KeyedVectors.load_word2vec_format(fileModel, binary=binary, unicode_errors='ignore')
        else:
            model = Word2Vec.load(fileModel)
        self.__model__ = model
        self.__userWords__ = []
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

    def isTrueConcept(self, userWords, parserWord):
        # if not self.__userWords__:
        #     for word in userWords:
        #         inflected = self.__morph__.parse(word)[0].inflect({'NOUN', 'sing', 'nomn'})
        #         if inflected:
        #             self.__userWords__.append(inflected.word)
        #         else:
        #             self.__userWords__.append(word)
        # inflectedParserWord = self.__morph__.parse(parserWord)[0].inflect({'NOUN', 'sing', 'nomn'})
        # if inflectedParserWord:
        #     parserWord = inflectedParserWord.word
        similarity = self.__model__.n_similarity([parserWord], userWords)
        return similarity > 0.3

    def trainFile(self, filename, encoding='utf8'):
        text = open(filename, 'r', encoding=encoding)
        lineSentence = LineSentence(text)
        oldMinCount = self.__model__.min_count
        self.__model__.min_count = 1
        self.__model__.build_vocab(lineSentence, update=True)
        self.__model__.min_count = oldMinCount
        self.__model__.train(lineSentence, total_examples=self.__model__.corpus_count, epochs=self.__model__.epochs)

    def getSimilarWords(self, words, grammems, count=10):
        wordInCache = self.__findWordInCache__(words)
        if wordInCache == False:
            wordlist = self.__mostSimilar__(words, topn=count * 10)
            finalWords = words.copy()
            for wordInList in wordlist:
                if len(finalWords) < count + len(words):
                    word_parse = self.__morph__.parse(wordInList[0])[0]
                    inflect = word_parse.inflect(grammems)
                    if inflect is not None and inflect.word not in finalWords:
                        finalWords.append(inflect.word)
            self.__cache__.append((words, finalWords))
            return finalWords
        else:
            return wordInCache[1]
