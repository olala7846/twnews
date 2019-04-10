#-*- coding: utf-8 -*-
import scrapy
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
}

MIN_P_TAGS = 3


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = [
        'www.chinatimes.com',
        'udn.com',
    ]
    start_urls = [
        # 'https://www.chinatimes.com/politic/',
        'https://udn.com',
    ]

    def parse(self, response):
        if not isinstance(response, HtmlResponse):
            print('response not html %s' % repsonse.url)

        parser = etree.HTMLParser()
        root = etree.HTML(response.text, parser)
        if self.is_article(root):
            print('%s is an article' % response.url)
        else:
            print('follow %s ' % response.url)
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

