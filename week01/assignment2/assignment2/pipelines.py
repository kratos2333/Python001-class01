# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd

class Assignment2Pipeline:
    def process_item(self, item, spider):
        movie_title = item['movie_title']
        movie_type = item['movie_type']
        release_date = item['release_date']
        output = str(movie_title) + '\t' + str(movie_type) + '\t' + str(release_date) + '\n'
        with open('./movie.csv','a+', encoding='UTF-8') as file:
            file.write(output)
        return item
