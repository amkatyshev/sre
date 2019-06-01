import sys
from ufal.udpipe import Model, Pipeline, ProcessingError
from gensim.models import Word2Vec, KeyedVectors
from conllu import parse_tree
import time
from SRE import SRE
from SRE.IOUtils import Output


start_time = time.time()

sre = SRE()
sre.analyze(['программирование'], 'testtext.txt')
sre.getResultByType('PART-OF', 'кодинг')


print(time.time() - start_time, 'execution time')
