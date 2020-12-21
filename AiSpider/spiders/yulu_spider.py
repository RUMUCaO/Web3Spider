# -*- coding: utf-8 -*-
# @Time    : 12/21/20 3:18 PM
# @Author  : yingyuankai
# @Email   : yingyuankai@aliyun.com
# @File    : xiaohua_spider.py
import scrapy
import json


class XiaoHuaSpider(scrapy.Spider):
    name = "yulu_spider"
    xiaohua_path = "./data/yulu__from_17989.txt"

    class_num = [
        ("http://www.17989.com/yulu/jingdian/{}.htm", "经典", 80),
        ("http://www.17989.com/duanyu/jingdian/{}.htm", "经典", 56),
        ("http://www.17989.com/yulu/lizhi/{}.htm", "励志", 50),
        ("http://www.17989.com/duanyu/lizhi/{}.htm", "励志", 58),
        ("http://www.17989.com/yulu/qinggan/{}.htm", "情感", 67),
        ("http://www.17989.com/yulu/zhengnengliang/{}.htm", "正能量", 42),
        ("http://www.17989.com/yulu/aiqing/{}.htm", "爱情", 56),
        ("http://www.17989.com/duanyu/aiqing/{}.htm", "爱情", 66),
        ("http://www.17989.com/yulu/xinqing/{}.htm", "心情", 49),
        ("http://www.17989.com/duanyu/duanyu/{}.htm", "心情", 74),
        ("http://www.17989.com/yulu/shanggan/{}.htm", "伤感", 46),
        ("http://www.17989.com/duanyu/shanggan/{}.htm", "伤感", 52),
        ("http://www.17989.com/yulu/weimei/{}.htm", "唯美", 36),
        ("http://www.17989.com/yulu/gaoxiao/{}.htm", "搞笑", 33),
        ("http://www.17989.com/duanyu/gaoxiao/{}.htm", "搞笑", 44),
        ("http://www.17989.com/yulu/leiren/{}.htm", "雷人", 35),
        ("http://www.17989.com/yulu/mingren/{}.htm", "名人", 60),
        ("http://www.17989.com/yulu/gexing/{}.htm", "个性", 45),
        ("http://www.17989.com/duanyu/gexing/{}.htm", "个性", 44),
        ("http://www.17989.com/duanyu/gexing/{}.htm", "祝福", 39),

    ]
    file_obj = open(xiaohua_path, "w")

    def start_requests(self):
        for itm in self.class_num:
            for i in range(1, itm[2]):
                cur_url = itm[0].format(i)
                meta = {"label": itm[1]}
                yield scrapy.Request(url=cur_url, callback=self.parser, meta=meta)

    def parser(self, response):
        meta = response.meta
        label = meta['label']
        lis = response.xpath("//div[@class='module articlelist']//li")
        for li in lis:
            content = li.xpath("./pre")
            if len(content) != 0:
                content = content[0].root.text
            else:
                continue
            item = {
                "content": content,
                "label": label
            }
            self.file_obj.write(json.dumps(item, ensure_ascii=False) + "\n")
