# -*- coding: utf-8 -*-
# @Time    : 12/21/20 3:18 PM
# @Author  : yingyuankai
# @Email   : yingyuankai@aliyun.com
# @File    : xiaohua_spider.py
import scrapy
import json


"""成语故事爬虫"""


class YuLuSpider(scrapy.Spider):
    name = "chenyu_spider"
    file_path = "./data/chenyu_gushi.txt"

    root_url = "http://www.hydcd.com/cy/chengyugushi.htm"
    base_url = "http://www.hydcd.com/cy/"
    file_obj = open(file_path, "a", encoding="utf8")

    pinyin_prefix = "【拼音】："
    jieshi_prefix = "【解释】："

    def start_requests(self):
        yield scrapy.Request(url=self.root_url, callback=self.first_page_parser)

    def first_page_parser(self, response):
        lis = response.xpath("//div[@align='left']//a")
        for itm in lis:
            href = itm.attrib.get("href")
            if href is None: continue
            if not href.startswith("gushi"): continue
            cur_url = self.base_url + href
            text = itm.root.text
            meta = {
                "text": text
            }
            yield scrapy.Request(url=cur_url, callback=self.second_page_parser, meta=meta)

    def second_page_parser(self, response):
        meta = response.meta
        chenyu_text = meta['text']
        ps = response.xpath("//div[@align='left']//p//text()").extract()
        ots = response.xpath("//div[@align='left']//font[@color='#10102C']//text()").extract()

        itm = {
            "chenyu": chenyu_text
        }
        for line in ps:
            if line.startswith(self.pinyin_prefix):
                pinyin = line[len(self.pinyin_prefix):].strip()
                itm['pinyin'] = pinyin
            elif line.startswith(self.jieshi_prefix):
                jieshi = line[len(self.jieshi_prefix):].strip()
                itm['jieshi'] = jieshi
            else:
                continue
        gushi = "\n".join([line.strip() for line in ots])
        itm['gushi'] = gushi
        new_line = json.dumps(itm, ensure_ascii=False) + "\n"
        self.file_obj.write(new_line)
