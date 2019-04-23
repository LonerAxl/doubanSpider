# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import settings
from scrapy.exporters import CsvItemExporter
from scrapy.exporters import JsonLinesItemExporter
from scrapy import signals
class DoubanspiderCSVPipeline(object):

    file = None
    exporter = None
    fields = ['subjectId', 'ISBN', 'title', 'subtitle', 'originalTitle', 'author', 'translator', 'image',
              'publisher',
              'pubdate', 'stackholder', 'pages', 'price', 'binding', 'series', 'summary', 'grade', 'gradedNum',
              'fiveStar',
              'fourStar', 'threeStar', 'twoStar', 'oneStar']
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        filename = 'outputs/'+ settings.CURRENT_TAG + '.csv'


        self.file = open(filename, 'a+b')
        self.exporter = CsvItemExporter(self.file, fields_to_export=self.fields, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):

        if settings.TAG_FLAG == 1:
            self.spider_closed(spider)
            self.spider_opened(spider)
        self.exporter.export_item(item)

        return item

    def serialize_field(self, field, name, value):
        return value.encode('utf-8')


class DoubanspiderJSONPipeline(object):
    file = None
    exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        filename = 'outputs/part' + str(settings.FILE_NAME_PART) + '.json'
        # filename = 'outputs/' + 'ua' + '.json'
        self.file = open(filename, 'a+b')
        self.exporter = JsonLinesItemExporter(self.file, encoding="utf-8", ensure_ascii=False )
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)

        return item
