"""Calculate TF and IDF
"""
from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol
from mrjob.protocol import BytesValueProtocol
from mrjob.protocol import TextProtocol
from mrjob.protocol import ReprProtocol
from nltk import ngrams
import re

# CSV_FILE = 'resource/chinatimes_20190409.csv'
CSV_FILE = 'resource/udn_20190410.csv'
STOP_WORDS = {'。', '的', '，', '|'}
N = 3


class MRWordFreqCount(MRJob):

  OUTPUT_PROTOCOL = ReprProtocol

  def mapper(self, _, line):
    word_bag = set()
    document = line.split(',')[0]
    for substr in document.split('|'):
      for ngram in ngrams(substr, N):
        word_bag.add(''.join(ngram))
    for word in word_bag:
      yield (word, 1)

  def reducer(self, word, counts):
    # yield (word, sum(counts))
    yield ("%05d" % sum(counts), word)


if __name__ == '__main__':
  MRWordFreqCount.run()
