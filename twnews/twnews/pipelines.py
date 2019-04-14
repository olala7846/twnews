# -*- coding: utf-8 -*-
#
# add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider.keys import PAGE_URL
from scrapy.exceptions import DropItem


class UrlDepupePipeline(object):

  def __init__(self):
    self.seen = set()

  def process_item(self, item, spider):
    # TODO(hcchao): send RPC to server, if should drop item
    # dedupe should be done before fire request.
    url = item[PAGE_URL]
    if url in self.seen:
      raise DropItem("Duplicate url %s" % url)
    else:
      self.seen.add(url)
      return item


class BigTablePipeline(object):
  """ Pipeline that writes data to bigtable """

  def open_spider(self, spider):
    # TODO(hcchao): connection to BT
    pass

  def close_spider(self, spider):
    # TODO(hcchao): close connection to BT
    pass

  def process_item(self, item, spider):
    # TODO(hcchao): write to big table

    return item
