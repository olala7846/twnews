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

MIN_ARTICLE_TAGS = 4
SPACE_CHARS = {'\n', '\r', '\t', '\v', ' '}
ARTICLE_TAGS = {'p', 'h1', 'h2', 'h3', 'h4', 'h5' }
PARAGRAPH_TAGS = {'article', 'title', 'header', 'h1', 'h2', 'h3', 'h4', 'h5', 'p', 'div'}
ADS_MIN_LEN = 10

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
        'https://www.chinatimes.com/opinion/20190409003973-262105?chdtv='
        'https://fund.udn.com/fund/story/5860/3703015'
        # 'https://www.chinatimes.com/politic/',
        # 'https://udn.com',
    ]

    def parse(self, response):
        if not isinstance(response, HtmlResponse):
            logging.warning('response not html %s' % repsonse.url)
            return

        parser = etree.HTMLParser()
        root = etree.HTML(response.text, parser)
        article_node = self.get_article_node(root)
        if article_node:
            content = self.scrape(article_node)
            yield {
              'content': content,
              'url': response.url,
            }
        else:
            # not article, follow links
            for href in response.css('a::attr(href)'):
              yield response.follow(href.get())

    def get_article_node(self, root):
        # A html DOM is an article if there is single node having more than
        # N <p></p> tags
        # Recursively traverse DOM tree to detect if it's a news article.
        def _find_article_node(node):
            if self._should_skip(node):
                return None

            num_p_tags = 0
            for sub_node in node:
                if sub_node.tag in ARTICLE_TAGS:
                    num_p_tags += 1
                if num_p_tags >= MIN_ARTICLE_TAGS:
                    return node

            # If root is not paragraph node, iterate through child nodes
            for sub_node in node:
                article_node = _find_article_node(sub_node)
                if article_node:
                    return article_node
            return None

        return _find_article_node(root)

    def scrape(self, root):
        content = ''
        def _traverse(node):
            nonlocal content

            if self._should_skip(node):
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

    def _should_skip(self, node):
        if node.tag is etree.Comment:
            return True

        if node.tag in IGNORE_TAGS:
            return True

        # Anchor tag having more than 20 characters are
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
