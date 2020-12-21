# -*- coding: utf-8 -*-
# @Time    : 12/21/20 3:18 PM
# @Author  : yingyuankai
# @Email   : yingyuankai@aliyun.com
# @File    : xiaohua_spider.py
import scrapy
import json


class JuziSpider(scrapy.Spider):
    name = "juzi_spider"
    xiaohua_path = "./data/juzi__from_17989.txt"

    class_num = [
        ("http://www.17989.com/juzi/weimei/{}.htm", "唯美", 109),
        ("http://www.17989.com/juzi/lizhi/{}.htm", "励志", 69),
        ("http://www.17989.com/juzi/shanggan/{}.htm", "伤感", 90),
        ("http://www.17989.com/juzi/zhengnengliang/{}.htm", "正能量", 56),
        ("http://www.17989.com/juzi/shangxin/{}.htm", "伤心", 57),
        ("http://www.17989.com/juzi/zheli/{}.htm", "哲理", 53),
        ("http://www.17989.com/juzi/beishang/{}.htm", "悲伤", 46),
        ("http://www.17989.com/juzi/gufeng/{}.htm", "古风", 32),
        ("http://www.17989.com/juzi/jingdian/{}.htm", "经典", 71),
        ("http://www.17989.com/juzi/aiqing/{}.htm", "爱情", 57),
        ("http://www.17989.com/juzi/youshang/{}.htm", "忧伤", 41),
        ("http://www.17989.com/juzi/wenyi/{}.htm", "文艺", 35),
        ("http://www.17989.com/juzi/sinian/{}.htm", "思念", 32),
        ("http://www.17989.com/juzi/shilian/{}.htm", "失恋", 27),
        ("http://www.17989.com/juzi/biaobai/{}.htm", "表白", 44),
        ("http://www.17989.com/juzi/xingfu/{}.htm", "幸福", 33),
        ("http://www.17989.com/juzi/shiwang/{}.htm", "失望", 26),
        ("http://www.17989.com/juzi/gaoxiao/{}.htm", "搞笑", 62),
        ("http://www.17989.com/juzi/anlian/{}.htm", "暗恋", 21),
        ("http://www.17989.com/juzi/huiyi/{}.htm", "回忆", 25),
        ("http://www.17989.com/juzi/xinlei/{}.htm", "心累", 23),
        ("http://www.17989.com/juzi/wunai/{}.htm", "无奈", 26),
        ("http://www.17989.com/juzi/xinfan/{}.htm", "心烦", 14),
        ("http://www.17989.com/juzi/xinsui/{}.htm", "心碎", 26),
        ("http://www.17989.com/juzi/shuqing/{}.htm", "抒情", 37),
        ("http://www.17989.com/juzi/houhui/{}.htm", "后悔", 17),
        ("http://www.17989.com/juzi/youqing/{}.htm", "友情", 33),
        ("http://www.17989.com/juzi/xinsuan/{}.htm", "心酸", 31),
        ("http://www.17989.com/juzi/yingyu/{}.htm", "英语", 43),
        ("http://www.17989.com/duanyu/yingyu/{}.htm", "英语", 48),
        ("http://www.17989.com/juzi/gaoxing/{}.htm", "高兴", 16),
        ("http://www.17989.com/juzi/xianshi/{}.htm", "现实", 34),
        ("http://www.17989.com/juzi/ganren/{}.htm", "感人", 31),
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
                "content": content,
                "label": label
            }
            self.file_obj.write(json.dumps(item, ensure_ascii=False) + "\n")
