# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
class W3CItem(Item):
    name=Field()
    parent=Field()
    link=Field()
    description=Field() 
class LanguageItem(Item):
    parent=Field()
    content=Field()
class TypeItem(Item):
    type=Field()#数字表示
    name=Field()
