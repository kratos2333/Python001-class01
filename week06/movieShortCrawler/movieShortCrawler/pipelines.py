# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class MovieshortcrawlerPipeline:
    def process_item(self, item, spider):
        comment_star = item['comment_star']
        comment_short = item['comment_short']

        # need to save to the database
        # output = str(movie_star) + ',' + str(movie_short) + ',' + str(date) + '\n'
        # with open('./comment.csv', 'a+', encoding='UTF-8') as file:
        #     file.write(output)
        # return item

        # prepare the insert sql
        insert_sql = f"INSERT INTO shorts (comment_star, comment_short) Values ( '{comment_star}','{comment_short}')"

        spider.insertShorts(insert_sql)

        return item
