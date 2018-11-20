# -*- coding: utf-8 -*-

import scrapy
from fitness_video.items import FitnessVideoItem


class MyScrapy(scrapy.Spider):
    """Crawl data"""

    name = "fitness_video"
    start_urls = [
        "https://www.hiyd.com/bb/692/"
    ]

    def parse(self, response):
        a_elements = response.xpath('//td[contains(@class, "tp-normal")]/a')
        if a_elements:
            for a_element in a_elements:
                url = a_element.xpath("@href").extract()[0]
                parent_id = a_element.xpath("div/text()").extract()[0]

                item = FitnessVideoItem()
                item["id"] = parent_id
                item["url"] = "http:" + url

                self.logger.info(item["url"])
                yield scrapy.Request(item["url"], meta={'item': item}, callback=self.detail_parse)

        self.logger.info("[+] Finish parse!")

    def detail_parse(self, response):
        self.logger.info("[+] Comming in detail parse!")
        item = response.meta['item']
        item["videos"] = list()

        for element in response.xpath("//li//div[contains(@class, 'cont-wrap')]"):
            video_item = FitnessVideoItem()
            video_item["id"] = element.xpath("div//span/text()").extract()[0]

            video_element = element.xpath("ul//a")[0]
            video_item["title"] = video_element.xpath("text()").extract()[0]
            video_item["url"] = "https://www.hiyd.com" + video_element.xpath("@href").extract()[0]

            item["videos"].append(video_item)

        self.logger.info(item)
        self.logger.info("[+] Finish detail parse!")
        return item

