import sys
from ufal.udpipe import Model, Pipeline, ProcessingError
from gensim.models import Word2Vec, KeyedVectors
from conllu import parse_tree
import time
from SRE import SRE

start_time = time.time()

sre = SRE()
sre.analyze('eloquentJS_ru.txt')


print(time.time() - start_time, 'execution time')
