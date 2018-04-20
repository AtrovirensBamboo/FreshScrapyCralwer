# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 17:41:09 2018

@author: 89288
"""

import scrapy
import json
import re
import time
from FirstScrapy.items import FirstscrapyItem
#from scrapy.contrib.loader import ItemLoader
#from scrapy.crawler import CrawlerProcess

class BasicSpider(scrapy.Spider):
    name = 'manual'
    allowed_domains = ['dpcq1.net']
    start_urls = ['http://www.dpcq1.net/1']
    
    def parse(self, response):
        
        #解析并返回要章节内容链接
        
        pre_href = 'http://www.dpcq1.net'
        
        #抽取主网页第一部分章节名及链接
        selectors_li_1 = response.xpath(
                                 ".//div[@class='card mt20 fulldir']//li")
        for selector_li_1 in selectors_li_1:
            title_1 = selector_li_1.xpath('./a/text()').extract()[0]
            href_end_1 = selector_li_1.xpath('./a/@href').extract()[0]
            href_1 = pre_href + href_end_1
            
            item = FirstscrapyItem(title=title_1,href=href_1)
            request_title = scrapy.Request(href_1,callback=self.parse_xhr,
                                           priority=1)
            #向子级response_xhr传递item信息
            request_title.meta['item'] = item
            
            yield request_title
        
        #抽取主网页第二部分章节名
        selectors_li_2 = response.xpath(
      './/div[@class="card mt20"]//ul[@class="dirlist three clearfix"]//li')
        for selector_li_2 in selectors_li_2:
            title_2 = selector_li_2.xpath('./a/text()').extract()[0]
            href_end_2 = selector_li_2.xpath('./a/@href').extract()[0]
            href_2 = pre_href + href_end_2
            
            item = FirstscrapyItem(title=title_2,href=href_1)
            request_title_2 = scrapy.Request(href_2,callback=self.parse_xhr,
                                             priority=1)
            #向子级response_xhr传递item信息
            request_title_2.meta['item'] = item
            
            yield request_title_2
    
    def parse_xhr(self,response_title):
        #解析网页中的xhr字符串
        
        #接收父级request_title传递的item信息
        item_xhr = response_title.meta['item']
        #解析XHR请求
        pre_xhr = 'http://www.dpcq1.net/novelsearch/reader/transcode/siteid/62/url/'
        xhr_end = response_title.xpath('.//script[last()]').re(
                                                            'url/(.*)?=')[0]
        xhr = pre_xhr + xhr_end + '='
        request_xhr = scrapy.Request(url=xhr,callback=self.parse_item,
                                     priority=2)
        #向子级response_content传递item元素
        request_xhr.meta['item'] = item_xhr
        yield request_xhr
        
    def parse_item(self,response_xhr):
        #解析网页中的文本
        
        #接受父级request_xhr传递的item信息
        item_content = response_xhr.meta['item']
        #抽取正文
        content_before = response_xhr.body.decode(response_xhr.encoding)
        dic_xhr = json.loads(content_before)
        content_middle = dic_xhr['info']
        content_after_1 = re.sub(r'<br/>','',content_middle)
        content_after = re.sub(r'\u3000','  ',content_after_1)
        
        item_content['content'] = content_after   
        
        yield item_content
        time.sleep(1)

'''
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl('dpcq')
    process.start()
'''
