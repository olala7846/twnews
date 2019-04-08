# parser.py
# We parse html page useing lxml instead of scrapy selector
# for reason, see the following link
# https://docs.scrapy.org/en/latest/topics/selectors.html#scrapy.selector.Selector

from lxml import etree  # Element Tree

# FILE_PATH = 'resource/chinatimes_sample.html'
# FILE_PATH = 'resource/udn.html'
FILE_PATH = 'resource/setn.html'
IGNORE_TAGS = {
  'audio',
  'button',
  'footer',
  'iframe',
  'meta',
  'nav',
  'script',
  'select',
  'style',
  'video',
}
IGNORE_CLASSES = {
  # 中時
  'comments',
  'gotop',
  'hot-news',
  'popin-recommend',
  'recommended-article',
  'social-share',
  # 聯合
  'listing',
  'menu',
  'only_web',
  'only_mobile',
  'social_bar',
  'social_more',
  'sitemap',
  # 三立
  'hidden-print',
  'sbNewsList',
}
IGNORE_IDS = {
  # 聯合
  'browser-update',
  'comments',
  'ec',
  'ec-body',
  'footer',
  'header',
  'msg',
  'next',
  'prev',
  'sidebar',
  'sidebar_attention_body',
  'toprow',
}

SECTION_TAGS = {'title', 'header', 'figure'}
SPACE_CHARS = {'\n', '\r', '\t', '\v', ' '}

def no_newline(string):
  for c in SPACE_CHARS:
    string = string.replace(c, '')
  return string

with open(FILE_PATH, 'r') as f:
  parser = etree.HTMLParser()
  html_text = f.read()
  root = etree.HTML(html_text, parser)

  html_text = ''
  def _traverse(node):
    global html_text

    # Skip html comments
    if node.tag is etree.Comment:
      return

    # Skip scripts, ads and meta
    if node.tag in IGNORE_TAGS:
      return

    # Skip recommened article
    if 'class' in node.attrib:
      node_classes = set(node.attrib['class'].split())
      if node_classes.intersection(IGNORE_CLASSES):
        return

    # Skip recommened article
    if 'id' in node.attrib and node.attrib['id'] in IGNORE_IDS:
      return

    if node.text:
      html_text = html_text + no_newline(node.text)
    for sub_node in node:
      _traverse(sub_node)
      if sub_node.tail:
        html_text = html_text + no_newline(sub_node.tail)
    if node.tag in SECTION_TAGS:
      html_text += '|'

  _traverse(root)
  print(html_text)
