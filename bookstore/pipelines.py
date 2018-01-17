# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BookstorePipeline(object):
    def __init__(self):
        self.file = open('bookstore.dat', 'wb')

    def process_item(self, item, spider):
        val = "{0}\t{1}\t{2}\n".format(item['rank'], item['title'], item['recommendation'])
        self.file.write(val)
        return item
