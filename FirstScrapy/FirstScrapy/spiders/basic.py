# -*- coding: utf-8 -*-
import scrapy
from FirstScrapy.items import FirstscrapyItem
#from scrapy.contrib.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

class BasicSpider(scrapy.Spider):
    name = 'dpcq'
    allowed_domains = ['dpcq1.net']
    start_urls = ['http://www.dpcq1.net/1']
    
    
    def parse(self, response):
        
        #解析并返回要爬取的内容
        
        pre_href = 'http://www.dpcq1.net'
        
        #抽取第一部分章节名及链接
        selectors_li_1 = response.xpath(
                                 ".//div[@class='card mt20 fulldir']//li")
        for selector_li_1 in selectors_li_1:
            title_1 = selector_li_1.xpath('./a/text()').extract()[0]
            href_end_1 = selector_li_1.xpath('./a/@href').extract()[0]
            href_1 = pre_href + href_end_1
            item_1 = FirstscrapyItem(title=title_1,href=href_1)
            yield item_1
        
        #抽取第二部分章节名
        selectors_li_2 = response.xpath(
      './/div[@class="card mt20"]//ul[@class="dirlist three clearfix"]//li')
        for selector_li_2 in selectors_li_2:
            title_2 = selector_li_2.xpath('./a/text()').extract()[0]
            href_end_2 = selector_li_2.xpath('./a/@href').extract()[0]
            href_2 = pre_href + href_end_2
            item_2 = FirstscrapyItem(title=title_2,href=href_2)
            yield item_2

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl('dpcq')
    process.start()

    
    
    
    
    
    
    
    
    
    
    
