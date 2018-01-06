# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo

from scrapy.exceptions import DropItem

class IgscraperPipeline(object):

    def __init__(self, mongo_uri, mongo_db, mongo_col):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_col = mongo_col
        self.ids_seen = set()

    @classmethod
    def from_crawler(cls, crawler):
        return cls (
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_col=crawler.settings.get('MONGO_COLLECTION'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['post_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" %item['post_id'])
        else:
            self.ids_seen.add(item['post_id'])
            self.db[self.mongo_col].insert(dict(item))
            logging.debug("post added to mongodb.")
            return item
