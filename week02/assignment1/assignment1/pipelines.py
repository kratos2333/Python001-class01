# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class Assignment1Pipeline:
    def process_item(self, item, spider):
        movie_title = item['movie_title']
        movie_type = item['movie_type']
        release_date = item['release_date']

        # prepare the insert sql
        insert_sql = f"INSERT INTO movies (movie_title, movie_type, release_date) Values ( '{movie_title}', '{movie_type}','{release_date}')"

        spider.insertMovie(insert_sql)

        return item
