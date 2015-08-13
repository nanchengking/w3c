# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3 as lite
from w3c.items import W3CItem, LanguageItem,TypeItem
from scrapy.item import Item

class W3CPipeline(object):
    
    def __init__(self):
        self.setupDBCon()
        self.createTables()
        
    def process_item(self, item, spider):
        
        if(isinstance(item, TypeItem)):
            self.storeInTypeTable(item)          
        
        if(isinstance(item, LanguageItem)):
            self.storeInLanguageItemTable(item)
            
        if(isinstance(item, W3CItem)):
            self.storeInW3CTable(item)
                      
        return item
    
    
    def storeInTypeTable(self, item):
        self.cur.execute("INSERT INTO type(\
            type, \
            name\
            ) \
        VALUES( ?, ? )", \
        ( \
            item.get('type', 0), 
            item.get('name', '')
        ))
        self.con.commit() 
        
    def storeInLanguageItemTable(self, item):
        self.cur.execute("INSERT INTO language(\
            code,\
            type, \
            name,\
            link\
            ) \
        VALUES( ?, ?,?,? )", \
        ( \
            item.get('code', 0), 
            item.get('type', 0),
            item.get('name', ''),
            item.get('link', '')
        ))
        self.con.commit() 
        
    def storeInW3CTable(self,item):
        print '----type()',type(item.get('code', 0)),item.get("code", 0)
        j=item.get("code", 0)
        self.cur.execute("INSERT INTO w3c(\
            name,\
            link, \
            nextLink,\
            prevLink,\
            description,\
            code\
            ) \
        VALUES(?,?,?,?,?,?)", \
        ( \
            item.get('name', ''), 
            item.get('link', ''),
            item.get('nextLink', ''),
            item.get('prevLink', ''),
            item.get('description', ''),
            j
        ))
        self.con.commit() 
        
    def setupDBCon(self):
        self.con = lite.connect('w3c.db')
        self.cur = self.con.cursor()
        
    def createTables(self):
        self.dropW3CTable()
        self.dropTypeTable()
        self.dropLanguageTable()
        self.createW3CTable()
        self.createTypeTable()
        self.createLanguageTableTable()
    def dropW3CTable(self):
        self.cur.execute("DROP TABLE IF EXISTS w3c")

    def dropLanguageTable(self):
        self.cur.execute("DROP TABLE IF EXISTS language") 
    def dropTypeTable(self):
        self.cur.execute("DROP TABLE IF EXISTS type") 
        
    def createW3CTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS w3c(id INTEGER PRIMARY KEY NOT NULL, \
            name TEXT, \
            link TEXT, \
            code INTEGER NOT NULL,\
            prevLink TEXT,\
            nextLink TEXT, \
            description TEXT\
            )")

    def createTypeTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS type(id INTEGER PRIMARY KEY NOT NULL, \
            type INTEGER NOT NULL, \
            name TEXT\
            )")
    def createLanguageTableTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS language(id INTEGER PRIMARY KEY NOT NULL, \
            type INTEGER NOT NULL, \
            name TEXT,\
            code INTEGER NOT NULL,\
            link TEXT\
            )")
        
    def  close_spider(self,spider):
        print '===spider is closed!!!==='
        self.con.close()
