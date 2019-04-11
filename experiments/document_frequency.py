"""The classic MapReduce job: count the frequency of words.
"""
from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol
from mrjob.protocol import BytesValueProtocol
from mrjob.protocol import TextProtocol
from mrjob.protocol import ReprProtocol
import re

CSV_FILE = 'resource/chinatimes_20190409.csv'
STOP_WORDS = {'。', '的', '，', '|'}


class MRWordFreqCount(MRJob):

  OUTPUT_PROTOCOL = ReprProtocol

  def mapper(self, _, line):
    content = line.split(',')[0]
    for substr in content.split('|'):
      if substr:
        yield (substr, 1)

  def reducer(self, word, counts):
    # yield (word, sum(counts))
    yield ("%05d" % sum(counts), word)


if __name__ == '__main__':
  MRWordFreqCount.run()
