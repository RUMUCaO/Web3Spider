# -*- coding: utf-8 -*-
# @Time    : 12/21/20 3:18 PM
# @Author  : yingyuankai
# @Email   : yingyuankai@aliyun.com
# @File    : xiaohua_spider.py

import scrapy
from bs4 import BeautifulSoup
import requests


"""新闻爬虫"""

class NewsSpider(scrapy.Spider):
    name = "news"
    file_path = "./data/News.txt"
    url = "https://chainnews-archive.org/"

    def start_requests(self):
        for i in range(2, 1544):
            cur_url = self.url + "/page/" + str(i)
            yield scrapy.Request(cur_url, self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', {'class': 'post-entry'})

        # 打开文件并写入文章标题、内容、日期和来源链接
        with open(self.file_path, 'w', encoding='utf-8') as file:
            for article in articles:
                header = article.find("header", class_="entry-header")
                title = header.find("h2").text.strip()
                content = article.find("section", class_="entry-content").text.strip()
                date = article.find("footer", class_="entry-footer").find("span").get("title")
                link = article.find("a", class_="entry-link").get("href")
                file.write(f'{str(header)}\n{title}\n{content}\n{date}\n{link}\n\n')
