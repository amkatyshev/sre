from gensim.models import Word2Vec, KeyedVectors
from pymorphy2 import MorphAnalyzer


class Model(object):
    def __init__(self, fileModel, isVector=False, binary=False):
        self.__morph__ = MorphAnalyzer()
        if isVector:
            model = KeyedVectors.load_word2vec_format(fileModel, binary=binary)
        else:
            model = Word2Vec.load(fileModel)
        self.__model__ = model

    def __mostSimilar__(self, word, topn=10):
        return self.__model__.wv.most_similar(word, topn=topn)

    def getSimilarWords(self, word, count):
        wordlist = self.__mostSimilar__(word, topn=50)
        main_word = self.__morph__.parse(word)[0]
        final_words = [main_word.normal_form]
        for word in wordlist:
            word_parse = self.__morph__.parse(word[0])[0]
            if 'VERB' in main_word.tag and word_parse.normal_form != main_word.normal_form and main_word.tag.person == word_parse.tag.person:
                final_words.append(self.__morph__.parse(word[0])[0].normal_form)
        return final_words[:count + 1]
