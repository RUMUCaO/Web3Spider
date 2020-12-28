# -*- coding: utf-8 -*-
# @Time    : 12/21/20 3:18 PM
# @Author  : yingyuankai
# @Email   : yingyuankai@aliyun.com
# @File    : xiaohua_spider.py
import scrapy
import json
import os
from urllib.request import urlretrieve


class DongtuSpider(scrapy.Spider):
    name = "gaoxiao_dongtu_spider"

    class_num = [
        ("http://www.17989.com/dongtaitu/", "gif", 1392)
    ]
    img_path = "./data/gifs/"

    def start_requests(self):
        for itm in self.class_num:
            for i in range(1, itm[2]):
                cur_url = itm[0].format(i)
                meta = {"type": itm[1]}
                yield scrapy.Request(url=cur_url, callback=self.parser, meta=meta)

    def parser(self, response):
        meta = response.meta
        type = meta['type']
        lis = response.xpath("//div[@class='module articlelist']//li")
        for li in lis:
            title = li.xpath("./div[@class='hd']")
            if len(title) != 0:
                title = title[0].root.text
            else:
                continue
            content = li.xpath(".//img")
            if len(content) != 0:
                content = content.attrib['src']
            else:
                continue

            cur_path = os.path.join(self.img_path, f"{title}.{type}")
            urlretrieve(content, cur_path)