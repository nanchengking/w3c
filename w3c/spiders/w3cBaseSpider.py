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
        "http://www.runoob.com/" # this is the main page of w3c /html/body/section/div[2]/div[1]/a[1]/strong
    ] 
    
    def parse(self, response):
        self.type=0
        self.code=0
        self.wanted_num=2
        for sel in response.xpath("//section[@class='container container-page']/div[@class='content']/div[@class]"):
            typeItem=TypeItem()
            typeItem['name']=sel.xpath('h2/text()').extract()[0]
            typeItem['type']=self.type
            
            self.type+=1
            for mSel in sel.xpath('a'):
                self.code+=1
                languageItem=LanguageItem()
                languageItem['code']=self.code
                languageItem['type']=self.type
                languageItem['link']='http://www.runoob.com/'+mSel.xpath('@href').extract()[0]
                languageItem['name']=mSel.xpath('h4/text()').extract()[0]
                request = scrapy.Request(languageItem['link'], callback=self.parseLanguageItem)
                request.meta['item'] = languageItem
                yield request
            print "===name is",typeItem['name'],type(typeItem['name']),'===numb:',self.type 
            #request = scrapy.Request(typeItem['MianPageUrl'], callback=self.parseMovieDetails)
            #request.meta['item'] = item
            #yield request
            if(self.type>=self.wanted_num):
                return
            yield typeItem    
        print "==finish!!!=="
    def parseLanguageItem(self,response):
        item = response.meta['item']
        sel = response.xpath("//div[@id='main']")
        w3cItem=W3CItem() 
        i=item['code']
        w3cItem['code']=item['code']
        print '===code type is: ',type(w3cItem['code'])
        w3cItem['link']=response.url
        w3cItem['name']=sel.xpath("div[@id='content']/h1/text()").extract()+sel.xpath("div[@id='content']/h1/span/text()").extract()
        w3cItem['nextLink']=sel.xpath("div[@class='chapter']/div[@class='next']/a[@href]/@href").extract()
        w3cItem['prevLink']=sel.xpath("div[@class='chapter']/div[@class='prev']/a[@href]/@href").extract()
        w3cItem['description']=sel.xpath("div[@id='content']").extract()
        yield w3cItem 
        yield item
        
