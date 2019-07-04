# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    positionName = scrapy.Field()
    positionFrom = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    education = scrapy.Field()
    workYear = scrapy.Field()
    update_time= scrapy.Field()
    companyName = scrapy.Field()
    companyLink = scrapy.Field()
    industryField = scrapy.Field()
    positionLink = scrapy.Field()
    positionDescription = scrapy.Field()
    companySize = scrapy.Field()
    pass
