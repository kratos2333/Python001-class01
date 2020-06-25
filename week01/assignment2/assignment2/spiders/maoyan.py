# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from assignment2.items import Assignment2Item

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    # def start_requests(self):
    #     url = 'https://maoyan.com/films?showType=3'
    #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pipline_items = []

        # select each movie
        movies = Selector(response=response).xpath('//div[@class="movie-item film-channel"]')
        for movie in movies[:10]:
            title_and_type = movie.xpath('.//div[@class="movie-hover-title"]')
            release_date = movie.xpath('.//div[@class="movie-hover-title movie-hover-brief"]')

            movie_title_selector = title_and_type[0].xpath('./@title')
            movie_title = movie_title_selector.extract_first()
            movie_type_selector = title_and_type[1].xpath('./text()')
            movie_type = movie_type_selector.extract()[1].strip()
            release_date_selector = release_date[0].xpath('./text()')
            release_date = release_date_selector.extract()[1].strip()

            # init new item for each movie
            item = Assignment2Item()
            item['movie_title'] = movie_title
            item['movie_type'] = movie_type
            item['release_date'] = release_date
            print(movie_title)
            print(movie_type)
            print(release_date)
            pipline_items.append(item)
        print(pipline_items)
        return pipline_items