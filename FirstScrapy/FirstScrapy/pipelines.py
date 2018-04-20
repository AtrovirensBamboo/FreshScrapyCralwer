# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy.exceptions import DropItem

class FirstscrapyPipeline(object):
    
    def __init__(self):
        self.client = pymongo.MongoClient('localhost',27017)
        self.database = self.client.dpcq
    
    def process_item(self, item, spider):
        
        try:
            collection_urls = self.database.dic_contents
            collection_urls.insert(item)
            return item
        except:
            raise DropItem('Datas save failed')
    
    def close_spider(self,spider):
        self.client.close()

        
