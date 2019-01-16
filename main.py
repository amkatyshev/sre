import sys
from ufal.udpipe import Model, Pipeline, ProcessingError
from conllu import parse_tree
import time

start_time = time.time()
model = Model.load('russian-syntagrus-ud-2.3-181115.udpipe')

pipeline = Pipeline(model, 'horizontal', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')

error = ProcessingError()
processed_conllu = pipeline.process(line, error)
print(processed_conllu)
