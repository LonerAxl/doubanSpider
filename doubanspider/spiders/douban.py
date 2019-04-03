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
#         print(info)
        infose = Selector(text=info)
        # print(infose.css("#info::text").extract())
        # print(infose.css("#info>span.pl").extract())
        attr = infose.css("#info>span.pl::text").extract()
        value = infose.css("#info::text").extract()
        # print(attr)
        # print(value)
        dic=[]
        try:
            attr.remove('出品方:')
        except ValueError:
            pass

        try:
            attr.remove('丛书:')
        except ValueError:
            pass
        for i in range(len(attr)):
            dic.append((attr[i],value[i]))
        dic.append(('标题:', infose.css("a.nbg::attr(title)").extract_first()))
        dic.append(('图片:', infose.css("a.nbg::attr(href)").extract_first()))
        stars = infose.css("span.rating_per::text").extract()
        if len(stars) != 0:
            for i in range(len(stars)):
                dic.append((5-i, stars[i]))

        dic.append(('总分:', infose.css("strong.ll.rating_num::text").extract_first()))
        dic.append(('总人数:', infose.css("#interest_sectl>div>div>div>div.rating_sum>span>a>span::text").extract_first()))

        summary = re.sub(">\s*<", "><", response.css('div.intro').extract_first())
        #         print(info)
        summaryse = Selector(text=summary)
        dic.append(('简介:', summaryse.css("p::text").extract_first()))
        for i in dic:
            print(i)

        # content > div > div.article > div.indent > div.subjectwrap.clearfix
        # print(response.headers)

    def start_requests(self):
        url = 'https://book.douban.com/subject/30372880/'
        url2 = 'https://book.douban.com/subject/30487959/'
        yield scrapy.Request(url=url2, callback=self.parse, dont_filter=True)
