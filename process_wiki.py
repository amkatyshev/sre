from __future__ import print_function
from tqdm import tqdm
import sys
from gensim.corpora import WikiCorpus


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


if __name__ == '__main__':
    getWikiTexts('ruwiki-20190501-pages-articles.bz2', 'ruwiki.txt')
