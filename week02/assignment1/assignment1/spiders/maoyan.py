# -*- coding: utf-8 -*-
import scrapy
import pymysql
from assignment1.items import Assignment1Item
from assignment1.NoMovieFoundException import NoMovieFoundException

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                                    port=3306,
                                    user='real_user',
                                    password='real_password',
                                    database='pythonCamp',
                                    charset='utf8mb4')
        self.cursor = self.conn.cursor()

    def insertMovie(self, insert_sql):
        self.cursor.execute(insert_sql)

    def parse(self, response):
        pipline_items = []

        try:
            # select each movie
            movies = response.xpath('//div[@class="movie-item film-channel"]')
            if len(movies) == 0:
                raise NoMovieFoundException('no movie found')
            for movie in movies[:10]:
                movie_infos = movie.xpath('.//div[contains(@class,"movie-hover-title")]')

                movie_title_selector = movie_infos[0].xpath('./@title')
                movie_title = movie_title_selector.extract_first()
                movie_type_selector = movie_infos[1].xpath('./text()')
                movie_type = movie_type_selector.extract()[1].strip()
                release_date_selector = movie_infos[3].xpath('./text()')
                release_date = release_date_selector.extract()[1].strip()

                # init new item for each movie
                item = Assignment1Item()
                item['movie_title'] = movie_title
                item['movie_type'] = movie_type
                item['release_date'] = release_date

                pipline_items.append(item)
        except NoMovieFoundException as nmfe:
            print("Please double check the xpath")
            print(nmfe)
        return pipline_items

    # close database connection
    def __del__(self):
        self.cursor.close()
        self.conn.close()
