# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
class W3CItem(Item):
    name=Field()#这一章的名字
    code=Field()#对应Language的code
    link=Field()#这一页本身的连接
    nextLink=Field()#这一页的下一页连接
    description=Field() #这一页的内容
class LanguageItem(Item):
    code=Field()#每一种语言的唯一标识符
    name=Field()#每一种语言的名字
    type=Field()#对应TypeItem的type
    link=Field()#对应的第一个连接，应该就是一个w3cItem的连接
class TypeItem(Item):
    type=Field()#数字表示
    name=Field()#属于前端？服务端？
