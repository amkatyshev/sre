from __future__ import print_function
import sys
import multiprocessing
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec, KeyedVectors
from gensim.models.word2vec import LineSentence
from tqdm import tqdm
from pymorphy2 import MorphAnalyzer
from pprint import pprint
from SRE import Model


def getWikiTexts(input_wikidata, output_wikitext='wiki.txt'):
    output = open(output_wikitext, 'w', encoding='utf8')
    print('Analyzing wikidata...')
    wiki = WikiCorpus(input_wikidata, lemmatize=False, dictionary={})
    print('Saving wiki content...')
    i = 0
    for text in tqdm(wiki.get_texts(), file=sys.stdout):
        output.write(' '.join(text) + "\n")
        i = i + 1
        if i % 1000 == 0:
            print(' Saved ' + str(i) + ' articles', end='\n')
    output.close()


def createVectorsFromtext(text, out_model='data.model', out_vectors='data.vec'):
    print('Create model...', end=' ')
    model = Word2Vec(
        LineSentence(text),
        size=100,
        sg=1,
        min_count=5,
        window=5,
        iter=10,
        workers=max(1, multiprocessing.cpu_count() - 1)
    )
    print('[OK]', end='\n')
    print('Save model...', end=' ')
    model.save(out_model)
    model.wv.save_word2vec_format(out_vectors, binary=False)
    print('[OK]', end='\n')
    return model


def getModel(filemodel):
    print('Get model ' + filemodel + '...', end=' ')
    model = Word2Vec.load(filemodel)
    print('[OK]', end='\n')
    return model


def getVectors(filevectors):
    print('Get model ' + filevectors + '...', end=' ')
    wv = KeyedVectors.load_word2vec_format(filevectors, binary=False)
    print('[OK]', end='\n')
    return wv


if __name__ == '__main__':
    morph = MorphAnalyzer()
    model = Model('wiki_new/wiki.model')
    wordlist = model.model.wv.most_similar('является', topn=40)
    main_word = morph.parse('является')[0]
    final_words = []
    for word in wordlist:
        word_parse = morph.parse(word[0])[0]
        if 'VERB' in main_word.tag and word_parse.normal_form != main_word.normal_form and main_word.tag.person == word_parse.tag.person:
            final_words.append(word)
    pprint(final_words)


