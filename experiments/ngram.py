#-*- coding: utf-8 -*-
import csv
from nltk import ngrams
from collections import Counter

CSV_FILE = 'resource/chinatimes_20190409.csv'
STOP_WORDS = {'。', '的', '，', '|'}


def split_text(text):
  l = 0
  for r in range(len(text)):
    if text[r] in STOP_WORDS:
      yield text[l:r]
      l = r + 1
  yield text[l:]

with open(CSV_FILE) as csv_file:
  csv_reader = csv.DictReader(csv_file, delimiter=',')
  word_counter = Counter()

  MAX_ROWS = 100
  i = 1
  for row in csv_reader:
    if i > MAX_ROWS:
      break
    i = i + 1
    print('parse article %d %s' % (i, row['url']))
    content = row['content']
    for part in split_text(content):
      grams = ngrams(part, 6)
      word_counter = word_counter + Counter(grams)

  results = []
  for word, count in word_counter.items():
    results.append((count, ''.join(word)))
  print(sorted(results))

# def clean_text(string):
#   for c in STOP_WORDS:
#     string = string.replace(c, '')
#   return string
#
# text = clean_text(TEXT)
#
# n = 2
# grams = ngrams(text, n)
# terms_count = {}
# for gram in grams:
#   term = ''.join(gram)
#   try:
#     terms_count[term] += 1
#   except KeyError:
#     terms_count[term] = 1
#
# results = []
# for key, val in terms_count.items():
#   results.append((val, key))
#
# print(sorted(results))
