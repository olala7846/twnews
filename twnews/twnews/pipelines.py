# -*- coding: utf-8 -*-
#
# add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .spiders.keys import PAGE_URL
from scrapy.exceptions import DropItem


class StoragePipeline(object):
  """ Pipeline that writes data to bigtable """

  def open_spider(self, spider):
    # Connect to Firestore, for deduplication
    # maybe create an API for this in the future?
    pass

  def close_spider(self, spider):
    # TODO(hcchao): close connection to BT
    # Close all connection
    pass

  def process_item(self, item, spider):
    # TODO(hcchao): write log to Firestore
    # TODO(hcchao): write html to Cloud Storage
    return item
