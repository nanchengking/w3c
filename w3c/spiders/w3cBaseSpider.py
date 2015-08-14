#coding=utf-8
'''
Created on 2015年8月11日

@author: Administrator
'''
import scrapy
import re
from w3c.items import W3CItem, LanguageItem,TypeItem
from bs4 import BeautifulSoup


class w3cSpider(scrapy.Spider):
    name = "w3cSpider"
    allowed_domains = ["runoob.com"]
    start_urls = [
        "http://www.runoob.com/" # this is the main page of w3c /html/body/section/div[2]/div[1]/a[1]/strong
    ] 
    
    def parse(self, response):
        self.j=0
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
    
            if(self.type>=self.wanted_num):
                #return
                pass
            yield typeItem    
        print "==finish!!!=="
    def parseLanguageItem(self,response):
        self.j+=1
        item = response.meta['item']
        sel = response.xpath("//div[@id='main']")
        w3cItem=W3CItem() 
        w3cItem['code']=item['code']
        baseUrl=re.match( r'^(.*\/)((.*?)html)$',response.url).group(1)
        print '===baseUrl is',baseUrl
        w3cItem['link']=response.url
        w3cItem['name']=''.join(sel.xpath("div[@id='content']/h1/text()").extract())+''.join(sel.xpath("div[@id='content']/h1/span/text()").extract()) 
        if(sel.xpath("div[@class='chapter']/div[@class='next']/a[@href]/@href").extract()):
            w3cItem['nextLink']=baseUrl+sel.xpath("div[@class='chapter']/div[@class='next']/a[@href]/@href").extract()[0]
        if(sel.xpath("div[@class='chapter']/div[@class='prev']/a[@href]/@href").extract()):
            w3cItem['prevLink']=baseUrl+sel.xpath("div[@class='chapter']/div[@class='prev']/a[@href]/@href").extract()[0]
        w3cItem['description']=self.getRideOfHtmlMarker(''.join(sel.xpath("div[@id='content']").extract()))
        request = scrapy.Request(w3cItem['nextLink'], callback=self.parseLanguageItem)
        request.meta['item'] = w3cItem
        if(self.j>=50):
            #return
            pass
        yield request
        yield item
    def getRideOfHtmlMarker(self,mStr):
        soup=BeautifulSoup(mStr)
        return ''.join(soup.findAll(text=True))
        
 
        
        
        
        
