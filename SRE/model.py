from gensim.models import Word2Vec, KeyedVectors


class Model(object):
    def __init__(self, fileModel, isVector=False, binary=False):
        if isVector:
            model = KeyedVectors.load_word2vec_format(fileModel, binary=binary)
        else:
            model = Word2Vec.load(fileModel)
        self.model = model
