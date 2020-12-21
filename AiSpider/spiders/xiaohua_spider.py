# -*- coding: utf-8 -*-
# @Time    : 12/21/20 3:18 PM
# @Author  : yingyuankai
# @Email   : yingyuankai@aliyun.com
# @File    : xiaohua_spider.py
import scrapy
import json


class XiaoHuaSpider(scrapy.Spider):
    name = "xiaohua_spider"
    root_url = "http://www.17989.com/xiaohua/{}.htm"
    xiaohua_path = "./data/xiaohua__from_17989.txt"

    class_num = [
        ("http://www.17989.com/xiaohua/lengxiaohua/{}.htm", "冷笑话", 1260),
        ("http://www.17989.com/xiaohua/youmo/{}.htm", "幽默笑话", 613),
        ("http://www.17989.com/xiaohua/ertong/{}.htm", "儿童笑话", 629),
        ("http://www.17989.com/xiaohua/exin/{}.htm", "恶心笑话", 48),
        ("http://www.17989.com/xiaohua/neihan/{}.htm", "内涵笑话", 257),
        ("http://www.17989.com/xiaohua/fuqi/{}.htm", "夫妻笑话", 580),
        ("http://www.17989.com/xiaohua/yingyu/{}.htm", "英语笑话", 83),
        ("http://www.17989.com/xiaohua/xiaoyuan/{}.htm", "校园笑话", 926),
        ("http://www.17989.com/xiaohua/nannv/{}.htm", "男女笑话", 277),
        ("http://www.17989.com/xiaohua/kongbu/{}.htm", "恐怖笑话", 68),
        ("http://www.17989.com/xiaohua/zonghe/{}.htm", "综合笑话", 1309),
        ("http://www.17989.com/xiaohua/baoxiao/{}.htm", "爆笑笑话", 534),
        ("http://www.17989.com/xiaohua/zhengren/{}.htm", "整人笑话", 121),
        ("http://www.17989.com/xiaohua/dongwu/{}.htm", "动物笑话", 116),
        ("http://www.17989.com/xiaohua/jingdian/{}.htm", "经典笑话", 207),
        ("http://www.17989.com/xiaohua/duanxiaohua/{}.htm", "短笑话", 154),
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
