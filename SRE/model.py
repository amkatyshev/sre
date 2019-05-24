from gensim.models import Word2Vec, KeyedVectors


class Model(object):
    def __init__(self, fileModel, isVector=False, binary=False):
        if isVector:
            model = KeyedVectors.load_word2vec_format(fileModel, binary=binary)
        else:
            model = Word2Vec.load(fileModel)
        self.__model__ = model

    def __mostSimilar__(self, word, topn=10):
        return self.__model__.wv.most_similar(word, topn=topn)
