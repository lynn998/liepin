# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import sqlite3
import os, re

class PipelineSqlite3(object):
    db_path = os.getcwd() + '/data/'
    db_file = db_path + 'liepin.sqlite3'
    table = 'liepin_jobs'
    if not os.path.exists(db_path):   #create 'data' path to store sqlite3 database file
        os.makedirs(db_path)
        
    def table_exists(self,con,table_name):
        sql = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{}'".format(table_name)
        con.execute(sql)
        fet = con.fetchall()
        exists = fet[0][0]
        return exists
        
        
    def process_item(self, item, spider):
        connect = sqlite3.connect(self.db_file)
        con = connect.cursor()
        table_name = self.table
        if (self.table_exists(con,table_name) == 0):
            sql = '''create table liepin_jobs(positionName varchar(500),
                        positionFrom varchar(20),salary varchar(100),city varchar(100),
                        education varchar(100),workYear varchar(100),update_time varchar(100),
                        companyName varchar(500),companyLink varchar(500),industryField varchar(500),
                        positionLink varchar(500),positionDescription varchar(8000),companySize varchar(100))'''
            con.execute(sql)
        positionName = item['positionName']
        positionFrom = item['positionFrom']
        salary = item['salary']
        city = item['city']
        education = item['education']
        workYear = item['workYear']
        update_time= item['update_time']
        companyName = item['companyName']
        companyLink = item['companyLink']
        industryField = item['industryField']
        positionLink = item['positionLink']
        positionDescription = item['positionDescription']
        companySize = item['companySize']
        sql = "insert into liepin_jobs (positionName,positionFrom,salary,city,education,workYear,update_time, companyName,companyLink,industryField,positionLink,positionDescription,companySize) \
                                            values (?,?,?,?,?,?,?,?,?,?,?,?,?)"
        con.execute(sql, (positionName,positionFrom,salary,city,education,workYear,\
                          update_time, companyName,companyLink,industryField,positionLink,positionDescription,companySize))
        connect.commit()
        con.close()
        connect.close()
# or
#sql = "insert into liepin_jobs values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(positionName,positionFrom,salary,city,education,workYear,update_time, companyName,companyLink,industryField,positionLink,positionDescription,companySize)
#con.execute(sql)

class GetLiepinPipeline(object):
    def table_exists(self,con,table_name):
        sql = "show tables;"
        con.execute(sql)
        tables = [con.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]
        if table_name in table_list:
            return 1
        else:
            return 0
        
    def process_item(self, item, spider):
        connect = pymysql.connect(
            user = 'you',
            password = '123456789',
            db = 'liepin',
            host = '127.0.0.1',
            port = 3306,
            charset = 'utf8'
            )
        con = connect.cursor()
        con.execute("use liepin")
        table_name = 'liepin_jobs'
        if (self.table_exists(con,table_name) != 1):
#            con.execute("drop table if exists liepin_jobs")
            sql = '''create table liepin_jobs( \
                    positionName varchar(500),positionFrom varchar(20),salary varchar(100),city varchar(100),
                    education varchar(100),workYear varchar(100),update_time varchar(100),
                    companyName varchar(500),companyLink varchar(500),industryField varchar(500),
                    positionLink varchar(500),positionDescription varchar(8000),companySize varchar(100))'''
            con.execute(sql) #如果不存在，创建表
        positionName = item['positionName']
        positionFrom = item['positionFrom']
        salary = item['salary']
        city = item['city']
        education = item['education']
        workYear = item['workYear']
        update_time= item['update_time']
        companyName = item['companyName']
        companyLink = item['companyLink']
        industryField = item['industryField']
        positionLink = item['positionLink']
        positionDescription = item['positionDescription']
        companySize = item['companySize']

        con.execute('insert into liepin_jobs(positionName,positionFrom,salary,city,education,workYear,update_time,\
                                            companyName,companyLink,industryField,positionLink,positionDescription,companySize) \
                                            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                            [positionName,positionFrom,salary,city,education,workYear,update_time,
                                             companyName,companyLink,industryField,positionLink,positionDescription,companySize])
        connect.commit()
        con.close()
        connect.close()



