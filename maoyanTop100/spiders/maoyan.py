# -*- coding: utf-8 -*-
import scrapy
from ..items import MaoYanItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4']

    def parse(self, response):
        movie_items = response.xpath("//dl[@class='board-wrapper']/dd")
        for movie_item in movie_items:
            item = MaoYanItem()
            item['index'] = movie_item.css(".board-index::text").extract_first()
            item['name'] = movie_item.xpath(".//p[@class='name']//text()").extract_first()
            item['star'] = movie_item.xpath(".//p[@class='star']//text()").extract_first()
            item['release_time'] = movie_item.xpath(".//p[@class='releasetime']//text()").extract_first()
            yield item

        next_page = response.xpath("//ul[@class='list-pager']//li[last()]//@href").extract_first()
        if 'offset' in next_page:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(next_url,callback=self.parse)