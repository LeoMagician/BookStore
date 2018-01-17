import scrapy
from scrapy.selector import Selector
from bookstore.items import BookstoreItem

class DangdangSpider(scrapy.Spider):
    name = "dangdang"
    allowed_domains = ["dangdang.com"]

    start_urls = [
        "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2017-0-1-1"
    ]

    def parse(self, response):
        page = Selector(response)

        hrefs = page.xpath('//li/div[@class="name"]/a/@href')

        for href in hrefs:
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        page = Selector(response)
        item = BookstoreItem()

        item["title"] = page.xpath('//div[@class="name_info"]/h1/text()').extract_first(default='not-found').encode("utf-8")
        item["url"] = response.url
        rank_name = page.xpath('//div[@class="pinglun"]/span[@class="t1"]/a/text()').extract_first(default='not-found').encode("utf-8")
        rank_num = page.xpath('//div[@class="pinglun"]/span[@class="t1"]/span[@class="num"]/text()').extract_first(default='not-found')
        item["rank"] = rank_name + rank_num
        item["comment"] = page.xpath('//a[@id="comm_num_down"]/text()').extract_first(default='not-found').encode("utf-8")


        divs = page.xpath('//div[@id="alsoBuy"]/div[@class="bucket"]/div[@class="over"]/ul[@class="none_b"]/div[@class="list_page"]')
        recom = ""

        for div in divs:
            lis = div.xpath('./li')
            for li in lis:
                # url = div.xpath('./p[@class="name"]/a/@href').extract_first()
                name = div.xpath('./p[@class="name"]/a/text()').extract_first(default='not-found').encode("utf-8")
                author = div.xpath('./p[@class="zuozhe"]/text()').extract_first(default='not-found').encode("utf-8")
                recom += "{0}:{1},".format(name, author)
                item["recommendation"] = recom
                yield item