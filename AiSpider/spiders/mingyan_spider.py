# -*- coding: utf-8 -*-
# @Time    : 12/21/20 3:18 PM
# @Author  : yingyuankai
# @Email   : yingyuankai@aliyun.com
# @File    : xiaohua_spider.py
import scrapy
import json


class MingYanSpider(scrapy.Spider):
    name = "mingyan_spider"
    root_url = "http://www.17989.com/xiaohua/{}.htm"
    xiaohua_path = "./data/mingyan__from_17989.txt"
    class_num = [
        ("http://www.17989.com/mingyan/lizhi/{}.htm", "励志名言", 49),
        ("http://www.17989.com/mingyan/mingren/{}.htm", "名人名言", 151),
        ("http://www.17989.com/mingyan/dushu/{}.htm", "读书名言", 37),
        ("http://www.17989.com/mingyan/jianchi/{}.htm", "坚持名言", 14),
        ("http://www.17989.com/mingyan/muai/{}.htm", "母爱名言", 14),
        ("http://www.17989.com/mingyan/aiguo/{}.htm", "爱国名言", 13),
        ("http://www.17989.com/mingyan/shijian/{}.htm", "时间名言", 18),
        ("http://www.17989.com/mingyan/zhexue/{}.htm", "哲学名言", 33),
        ("http://www.17989.com/mingyan/aiqing/{}.htm", "爱情名言", 39),
        ("http://www.17989.com/mingyan/zixin/{}.htm", "自信名言", 12),
        ("http://www.17989.com/mingyan/kuanrong/{}.htm", "宽容名言", 11),
        ("http://www.17989.com/mingyan/yingyu/{}.htm", "英语名言", 32),
        ("http://www.17989.com/mingyan/xinren/{}.htm", "信任名言", 15),
        ("http://www.17989.com/mingyan/youyi/{}.htm", "友谊名言", 18),
        ("http://www.17989.com/mingyan/mengxiang/{}.htm", "梦想名言", 23),
        ("http://www.17989.com/mingyan/hezuo/{}.htm", "合作名言", 9),
        ("http://www.17989.com/mingyan/zeren/{}.htm", "责任名言", 8),
        ("http://www.17989.com/mingyan/qinfen/{}.htm", "勤奋名言", 13),
        ("http://www.17989.com/mingyan/shengming/{}.htm", "生命名言", 13),
        ("http://www.17989.com/mingyan/jingdian/{}.htm", "经典名言", 39),
        ("http://www.17989.com/mingyan/leguan/{}.htm", "乐观名言", 9),
        ("http://www.17989.com/mingyan/ganen/{}.htm", "感恩名言", 12),
        ("http://www.17989.com/mingyan/anquan/{}.htm", "安全名言", 11),
        ("http://www.17989.com/mingyan/zuoren/{}.htm", "做人名言", 192),
        ("http://www.17989.com/mingyan/qianxu/{}.htm", "谦虚名言", 10),
        ("http://www.17989.com/mingyan/kexue/{}.htm", "科学名言", 10),
        ("http://www.17989.com/mingyan/xiaodao/{}.htm", "孝道名言", 11),
        ("http://www.17989.com/mingyan/fengxian/{}.htm", "奉献名言", 9),
        ("http://www.17989.com/mingyan/daode/{}.htm", "道德名言", 9),
        ("http://www.17989.com/mingyan/huanjing/{}.htm", "环境名言", 11),
        ("http://www.17989.com/mingyan/laodong/{}.htm", "劳动名言", 14),
        ("http://www.17989.com/mingyan/fuai/{}.htm", "父爱名言", 7),
        ("http://www.17989.com/mingyan/zhanzheng/{}.htm", "战争名言", 8),
        ("http://www.17989.com/mingyan/guyu/{}.htm", "古语名言", 33),
    ]
    file_obj = open(xiaohua_path, "a")

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
                "label": label,
                "content": content
            }
            self.file_obj.write(json.dumps(item, ensure_ascii=False) + "\n")
