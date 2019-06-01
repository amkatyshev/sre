import sys
from ufal.udpipe import Model, Pipeline, ProcessingError
from gensim.models import Word2Vec, KeyedVectors
from conllu import parse_tree
import time
from SRE import SRE
from SRE.IOUtils import Output
import os

start_time = time.time()

sre = SRE()
sre.analyze(['шаблон'], os.getcwd() + '/SRE/tests/testtext.txt')
sre.getResultByType('IS-A', 123)


print(time.time() - start_time, 'execution time')
