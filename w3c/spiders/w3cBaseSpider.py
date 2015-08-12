#coding=utf-8
'''
Created on 2015年8月11日

@author: Administrator
'''
import scrapy
import re
from w3c.items import W3CItem, LanguageItem,TypeItem


class w3cSpider(scrapy.Spider):
    name = "w3cSpider"
    allowed_domains = ["runoob.com"]
    start_urls = [
        "http://www.runoob.com" # this is the main page of w3c /html/body/section/div[2]/div[1]/a[1]/strong
    ] 
    
    def parse(self, response):
        self.typeCode=0
        self.wanted_num=100
        for sel in response.xpath("//section[@class='container container-page']/div[@class='content']/div"):
            typeItem=TypeItem()
            typeItem['name']=sel.xpath('h2/text()').extract()[0]
            typeItem['type']=self.typeCode;
            self.typeCode+=1
            print "===name is",typeItem['name'],type(typeItem['name']),'===numb:',self.typeCode
            
            #request = scrapy.Request(typeItem['MianPageUrl'], callback=self.parseMovieDetails)
            #request.meta['item'] = item
            #yield request
            if(self.typeCode>=self.wanted_num):
                return
            yield typeItem
        print "==finish!!!=="
