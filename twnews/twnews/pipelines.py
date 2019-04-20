# -*- coding: utf-8 -*-
#
# add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from .spiders.keys import CONTENT_HTML
from .spiders.keys import CRAWLED_TIME
from .spiders.keys import PAGE_URL
from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import unquote
from scrapy.exceptions import DropItem


ROOT_PATH = '/tmp/'


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
    url = urlparse(item[PAGE_URL])

    file_dir = '{}{}{}/'.format(ROOT_PATH, unquote(url.netloc), unquote(url.path))
    crawled_time = item[CRAWLED_TIME]
    assert(isinstance(crawled_time, datetime))
    file_name = crawled_time.strftime("%Y%m%d-%H%M%f") + '.html'
    file_path = file_dir + '/' + file_name

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, 'w') as f:
      f.write(item[CONTENT_HTML])

    item.pop(CONTENT_HTML, None)
    item['file_path'] = file_path

    return item
