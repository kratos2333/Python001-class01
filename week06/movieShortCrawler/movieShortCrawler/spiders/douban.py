# -*- coding: utf-8 -*-
import scrapy
import pymysql
from scrapy.selector import Selector
from movieShortCrawler.items import MovieshortcrawlerItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/subject/1308865/comments?sort=new_score&status=P']

    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                                    port=3306,
                                    user='root',
                                    password='password',
                                    database='db1',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def insertShorts(self, insert_sql):
        self.cursor.execute(insert_sql)
        self.conn.commit()

    def parse(self, response):
        rating_map = {'力荐': 5, '推荐': 4, '还行': 3, '较差': 2, '很差': 1}
        pipline_items = []

        # select each comment
        comments = Selector(response=response).xpath('//div[@class="comment"]')
        for comment in comments[:20]:

            # find the rating
            rating = 3
            rating_section = comment.xpath('.//span[contains(@class,"rating")]')
            if rating_section:
                rating = rating_map[str(rating_section.xpath('./@title').extract_first())]

            short = comment.xpath('.//span[@class="short"]/text()').extract_first().strip()

            # init new item for each movie short
            item = MovieshortcrawlerItem()
            item['comment_star'] = rating
            item['comment_short'] = short

            pipline_items.append(item)
        return pipline_items

    # close database connection
    def __del__(self):
        self.cursor.close()
        self.conn.close()

