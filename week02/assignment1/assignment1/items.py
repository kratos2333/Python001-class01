# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Assignment1Item(scrapy.Item):
    movie_title = scrapy.Field()
    movie_type = scrapy.Field()
    release_date = scrapy.Field()
