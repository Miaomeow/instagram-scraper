# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IgscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    post_id = scrapy.Field()
    is_video = scrapy.Field()
    caption = scrapy.Field()
    tags = scrapy.Field()
    likes = scrapy.Field()
    comments = scrapy.Field()
    date = scrapy.Field()
    media = scrapy.Field()
    pic = scrapy.Field()
