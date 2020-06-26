# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from assignment2.items import Assignment2Item

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        pipline_items = []

        # select each movie
        movies = Selector(response=response).xpath('//div[@class="movie-item film-channel"]')
        for movie in movies[:10]:
            movie_infos = movie.xpath('.//div[contains(@class,"movie-hover-title")]')

            movie_title_selector = movie_infos[0].xpath('./@title')
            movie_title = movie_title_selector.extract_first()
            movie_type_selector = movie_infos[1].xpath('./text()')
            movie_type = movie_type_selector.extract()[1].strip()
            release_date_selector = movie_infos[3].xpath('./text()')
            release_date = release_date_selector.extract()[1].strip()

            # init new item for each movie
            item = Assignment2Item()
            item['movie_title'] = movie_title
            item['movie_type'] = movie_type
            item['release_date'] = release_date

            pipline_items.append(item)
        return pipline_items