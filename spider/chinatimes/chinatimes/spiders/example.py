#-*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.http import HtmlResponse
from lxml import etree

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
  'ul',
  'li',
  'table',
  'tr',
  'td'
}

IGNORE_IDS = {
  'comments'
}

IGNORE_CLASSES = {
  'comments'
}

MIN_P_TAGS = 3
SPACE_CHARS = {'\n', '\r', '\t', '\v', ' '}
PARAGRAPH_TAGS = {'article', 'title', 'header', 'h1', 'h2', 'h3', 'h4', 'h5', 'p', 'div'}

def no_newline(string):
  for c in SPACE_CHARS:
    string = string.replace(c, '')
  return string

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = [
        'www.chinatimes.com',
        'udn.com',
    ]
    start_urls = [
        # 'https://www.chinatimes.com/opinion/20190409003973-262105?chdtv='
        'https://www.chinatimes.com/politic/',
        # 'https://udn.com',
    ]

    def parse(self, response):
        if not isinstance(response, HtmlResponse):
            logging.warning('response not html %s' % repsonse.url)
            return

        parser = etree.HTMLParser()
        root = etree.HTML(response.text, parser)
        if self.is_article(root):
            content = self.scrape(root)
            yield {
              'content': content,
              'url': response.url,
            }
        else:
            # not article, follow links
            for href in response.css('a::attr(href)'):
              yield response.follow(href.get())

    def is_article(self, root):
        # Recursively traverse DOM tree to detect if it's a news article.
        def _has_article_node(root):
            # Skip nodes that obviously doesn't include paragraph.
            if root.tag in IGNORE_TAGS:
                return False

            num_p_tag = 0
            for node in root:
                if node.tag == 'p':
                    num_p_tag += 1
                if num_p_tag >= MIN_P_TAGS:
                    return True

            # If root is not paragraph node, iterate through child nodes
            for node in root:
                if _has_article_node(node):
                    return True
            return False

        return _has_article_node(root)

    def scrape(self, root):
        content = ''
        def _traverse(node):
            nonlocal content

            if self.should_skip(node):
                return

            if node.text:
                content = content + no_newline(node.text)
            for sub_node in node:
                _traverse(sub_node)
                if sub_node.tail:
                    content = content + no_newline(sub_node.tail)
            # End of paragraph, add a seperator
            if node.tag in PARAGRAPH_TAGS:
                content += '|'

        _traverse(root)
        return content

    def should_skip(self, node):
        if node.tag is etree.Comment:
            return True

        if node.tag in IGNORE_TAGS:
            return True

        if 'id' in node.attrib and node.attrib['id'] in IGNORE_IDS:
          print('ignore id %s' % node.attrib['id'])
          return True

        if 'class' in node.attrib:
            for class_name in node.attrib['class'].split():
                if class_name in IGNORE_CLASSES:
                    print('ignore class %s' % class_name)
                    return True

        return False
