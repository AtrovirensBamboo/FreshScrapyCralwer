# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from FirstScrapy.items import FirstscrapyItem

class EasySpider(CrawlSpider):
    name = 'easy'
    allowed_domains = ['dpcq1.net']
    start_urls = ['http://www.dpcq1.net/1']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='.//*[@target="_blank"]'),
             follow=True,callback='parse_xhr'),
    )

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
            
            item = FirstscrapyItem(title=title_2,href=href_2)
            #向子级response_xhr传递item信息
            request_title_2.meta['item'] = item
            
            yield request_title_2
