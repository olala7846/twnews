#-*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['www.chinatimes.com']
    start_urls = ['https://www.chinatimes.com/politic/']

    def parse(self, response):
        print(response.url)
        for href in response.css('a::attr(href)'):
          yield response.follow(href.get())
