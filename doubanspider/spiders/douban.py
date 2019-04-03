# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Selector

class DoubanSpider(scrapy.Spider):
    name = 'douban'

    # allowed_domains = ['book.douban.com']
    allowed_domains = []
    start_urls = []

    def parse(self, response):

        info = re.sub(">\s*<","><",response.css('div.subjectwrap.clearfix').extract_first())
        print(info)
        infose = Selector(text=info)
        print(infose.css("#info::text").extract())
        # content > div > div.article > div.indent > div.subjectwrap.clearfix
        # print(response.headers)

    def start_requests(self):
        url = 'https://book.douban.com/subject/30372880/'

        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
