#-*- coding: utf-8 -*-
# Spider that crawl through new pages and downloads article html

import scrapy
import logging
from datetime import datetime
from scrapy.http import HtmlResponse
from lxml import etree
from .keys import PAGE_URL
from .keys import CONTENT_HTML
from .keys import CRAWLED_TIME

IGNORE_TAGS = {
  'audio',
  'button',
  'footer',
  'iframe',
  'li',
  'meta',
  'nav',
  'script',
  'select',
  'style',
  'table',
  'td'
  'tr',
  'ul',
  'video',
}

# Number of paragraphs required to be recognized as an article.
MIN_ARTICLE_TAGS_REQUIRED = 4
ARTICLE_TAGS = {'p', 'h1', 'h2', 'h3', 'h4', 'h5' }
ADS_MIN_LEN = 10


class NewsSpider(scrapy.Spider):
  name = 'news'
  allowed_domains = [
    'www.chinatimes.com',
    'udn.com',
  ]
  start_urls = [
    'https://www.chinatimes.com/opinion/20190409003973-262105?chdtv='
    # 'https://www.chinatimes.com/politic/',
    # 'https://fund.udn.com/fund/story/5860/3703015'
    # 'https://udn.com',
  ]

  def parse(self, response):
    if not isinstance(response, HtmlResponse):
      logging.warning('response not html %s' % repsonse.url)
      return

    if self.is_article(response):
      yield {
        PAGE_URL: response.url,
        CONTENT_HTML: response.text,
        CRAWLED_TIME: datetime.utcnow(),
      }

    else:
      # Follow links.
      for href in response.css('a::attr(href)'):
        yield response.follow(href.get())

  def is_article(self, response):
    parser = etree.HTMLParser()
    root = etree.HTML(response.text, parser)
    # A html DOM is an article if there is single node having more than
    # N <p></p> tags
    # Recursively traverse DOM tree to detect if it's a news article.
    def _has_article_node(node):
      if self._should_skip_node(node):
        return None

      num_article_nodes = 0
      for sub_node in node:
        if sub_node.tag in ARTICLE_TAGS:
          num_article_nodes += 1
        if num_article_nodes >= MIN_ARTICLE_TAGS_REQUIRED:
          return True

      # If root is not paragraph node, iterate through child nodes
      for sub_node in node:
        article_node = _has_article_node(sub_node)
        if article_node:
          return article_node
      return False

    return _has_article_node(root)

  def _should_skip_node(self, node):
    if node.tag is etree.Comment:
      return True

    if node.tag in IGNORE_TAGS:
      return True

    # Anchor tag having more than ADS_MIN_LEN characters are
    # usually advertisements or link to other article.
    if self._is_ads_or_link(node):
      return True

    return False

  def _is_ads_or_link(self, node):
    if node.tag != 'a':
      return False
    text = ''
    def _inner(node):
      nonlocal text
      if node.text:
        text += node.text
      for sub_node in node:
        _inner(sub_node)
        if sub_node.tail:
          text += sub_node.tail
    _inner(node)
    return len(text) >= ADS_MIN_LEN
