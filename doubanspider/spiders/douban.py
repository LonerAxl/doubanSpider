# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Selector
import numpy as np
import time
import settings



class DoubanSpider(scrapy.Spider):
    name = 'douban'

    allowed_domains = ['book.douban.com']
    # allowed_domains = []
    start_urls = []

    cur_lst = []

    def parse_detail(self, response):

        if response.css("#db-nav-book").extract_first() is None or response.css('div.subjectwrap.clearfix').extract_first() is None:
            return

        info = re.sub(">\s*<","><",response.css('div.subjectwrap.clearfix').extract_first())
        info = re.sub("[\s]{2,}", "", info)
        info = re.sub(">\s*/\s<*","><", info)
        info = re.sub(">\s*:\s<*", "><", info)
        infose = Selector(text=info)
        attr = infose.css("#info>span.pl::text").extract()
        value = infose.css("#info::text").extract()
        sp=[]
        item = Book()
        url_split = response.request.url.split('/')
        item['subjectId'] = url_split[-2]
        try:
            attr.remove('作者:')
            # sp.append('作者')
        except ValueError:
            pass

        try:
            attr.remove('出品方:')
            # sp.append('出品方')
        except ValueError:
            pass

        try:
            attr.remove('译者:')
            # sp.append('译者')
        except ValueError:
            pass

        try:
            attr.remove('丛书:')
            # sp.append('丛书')
        except ValueError:
            pass

        try:
            value.remove('/')
        except ValueError:
            pass
        print(value)

        for i in range(len(attr)):
            if attr[i] == '出版社:':
                item['publisher'] = value[i].strip()
            elif attr[i] == '副标题:':
                item['subtitle'] = value[i].strip()
            elif attr[i] == '出版年:':
                item['pubdate'] = value[i].strip()
            elif attr[i] == '页数:':
                item['pages'] = value[i].strip()
            elif attr[i] == '定价:':
                item['price'] = value[i].strip()
            elif attr[i] == '装帧:':
                item['binding'] = value[i].strip()
            elif attr[i] == 'ISBN:':
                item['ISBN'] = value[i].strip()
            elif attr[i] == '原作名:':
                item['originalTitle'] = value[i].strip()
        item['image'] = infose.css("a.nbg::attr(href)").extract_first().strip()
        item['title'] = response.css("#wrapper>h1>span::text").extract_first().strip()

        sp_val = infose.css("span + a::text").extract()
        sp = infose.xpath("//a/preceding-sibling::span[1]/text()").extract()
        # print(sp)
        # print(sp_val)
        try:
            sp_val.remove('人评价')
        except ValueError:
            pass

        for i in range(len(sp_val)):
            if sp[i] == '作者:':
                item['author'] = sp_val[i].strip()
            elif sp[i] == '出品方:':
                item['stackholder'] = sp_val[i].strip()
            elif sp[i] == '译者:':
                item['translator'] = sp_val[i].strip()
            elif sp[i] == '丛书:':
                item['series'] = sp_val[i].strip()

        sp_a = infose.css("#info>span:not(.pl)").extract()
        for i in range(len(sp_a)):
            sec = Selector(text=sp_a[i])
            cur = sec.css("span.pl::text").extract_first().strip()
            if cur == '作者':
                item['author'] = ', '.join(sec.css("a::text").extract())
            elif cur == '出品方':
                item['stackholder'] = ', '.join(sec.css("a::text").extract())
            elif cur == '译者':
                item['translator'] = ', '.join(sec.css("a::text").extract())
            elif cur == '丛书':
                item['series'] = ', '.join(sec.css("a::text").extract())

        stars = infose.css("span.rating_per::text").extract()
        if len(stars) != 0:
            for i in range(len(stars)):
                if i == 0:
                    item['fiveStar'] = stars[i]
                elif i == 1:
                    item['fourStar'] = stars[i]
                elif i == 2:
                    item['threeStar'] = stars[i]
                elif i == 3:
                    item['twoStar'] = stars[i]
                elif i == 4:
                    item['oneStar'] = stars[i]

        grade = infose.css("strong.ll.rating_num::text").extract_first()
        if grade is not None :
            item['grade'] = grade.strip()
        gradedNum = infose.css("#interest_sectl>div>div>div>div.rating_sum>span>a>span::text").extract_first()
        if gradedNum is not None:
            item['gradedNum'] = gradedNum.strip()

        if response.css('div.intro').extract_first() is not None:
            summary = re.sub(">\s*<", "><", response.css('div.intro').extract_first())
            summaryse = Selector(text=summary)
            item['summary'] = ''.join(summaryse.css("p::text").extract()).strip()
        print(response.request.headers)
        yield item

    def start_requests(self):

        for i in range(settings.START_NUM,settings.END_NUM):
            yield scrapy.Request(url='https://book.douban.com/subject/'+str(i)+'/', callback=self.parse_detail)
            # time.sleep(np.random.rand() * 5)



class Book(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    stackholder = scrapy.Field()
    subtitle = scrapy.Field()
    originalTitle = scrapy.Field()
    translator = scrapy.Field()
    pubdate = scrapy.Field()
    pages = scrapy.Field()
    price = scrapy.Field()
    binding = scrapy.Field()
    series = scrapy.Field()
    ISBN = scrapy.Field()
    summary = scrapy.Field()
    fiveStar = scrapy.Field()
    fourStar = scrapy.Field()
    threeStar = scrapy.Field()
    twoStar = scrapy.Field()
    oneStar = scrapy.Field()
    grade = scrapy.Field()
    gradedNum = scrapy.Field()
    subjectId = scrapy.Field()


class UASpider(scrapy.Spider):
    name = 'uaspider'

    allowed_domains = ['developers.whatismybrowser.com']
    # allowed_domains = []
    start_urls = []

    def parse(self, response):
        if response.css("div.content-base>section>div").extract_first() is None:
            return
        div = re.sub(">\s*<","><",response.css('div.content-base>section>div').extract_first())
        div = re.sub("[\s]{2,}", "", div)
        div = re.sub(">\s*/\s<*","><", div)
        div = re.sub(">\s*:\s<*", "><", div)


        rows = Selector(text=div).css('table>tbody>tr').extract()

        for row in rows:
            s = Selector(text=row)
            content = s.css('td::text').extract()
            if content[2] == "Computer":
                ua = s.css('td.useragent>a::text').extract_first()
                yield {'useragent':ua}
        page = Selector(text=div).css('#pagination>a').extract()
        url = Selector(text=page[-2]).css('::attr(href)').extract_first()
        if Selector(text=div).css('#pagination>span.current::text').extract_first() == '10':
            return
        yield scrapy.Request(url=response.urljoin(url), callback=self.parse)

    def start_requests(self):
        url = "https://developers.whatismybrowser.com/useragents/explore/software_name/outlook/"
        yield scrapy.Request(url=url, callback=self.parse)

