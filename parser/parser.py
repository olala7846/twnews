# parser.py
# We parse html page useing lxml instead of scrapy selector
# for reason, see the following link
# https://docs.scrapy.org/en/latest/topics/selectors.html#scrapy.selector.Selector

from lxml import etree  # Element Tree

FILE_PATH = 'resource/chinatimes_sample.html'

with open(FILE_PATH, 'r') as f:
  parser = etree.XMLParser()
  html_text = f.read()
  root = etree.parse(html_text, parser)
  print(root)

  #TODO(hcchao): draw tree node

