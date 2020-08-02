# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieshortcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    comment_star = scrapy.Field()
    comment_short = scrapy.Field()
