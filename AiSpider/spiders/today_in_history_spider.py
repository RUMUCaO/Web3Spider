# -*- coding: utf-8 -*-
# @Time    : 12/21/20 3:18 PM
# @Author  : yingyuankai
# @Email   : yingyuankai@aliyun.com
# @File    : xiaohua_spider.py
import scrapy
import json


class TodayInHistorySpider(scrapy.Spider):
    name = "today_in_history_spider"
    txt_path = "./data/today_in_history.txt"
    root_url = "http://today.911cha.com/history_{}.html"
    base_url = 'http://today.911cha.com/'
    file_obj = open(txt_path, "a")

    def start_requests(self):
        for i in range(1, 367):
            cur_url = self.root_url.format(i)
            yield scrapy.Request(url=cur_url, callback=self.parser)

    def parser(self, response):
        lis = response.xpath("//p[@class='f14 l150']//a")
        for i in range(0, len(lis), 3):
            year_text = lis[i + 0].root.text

            day_in_year = lis[i + 1].root.text

            story = lis[i + 2].root.text

            story_url = lis[i + 2].attrib['href']

            cur_story_url = self.base_url + story_url

            meta = {
                "year": year_text,
                "day": day_in_year,
                "event": story
            }

            yield scrapy.Request(url=cur_story_url, callback=self.parser_story_page, meta=meta)

    def parser_story_page(self, response):
        meta = response.meta
        story = response.xpath("//p[@class='f14']//text()").extract()

        item = {
            "year": meta['year'],
            "day": meta['day'],
            "title": meta['event'],
            "context": story
        }
        self.file_obj.write(json.dumps(item, ensure_ascii=False) + "\n")
