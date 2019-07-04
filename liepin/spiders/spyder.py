import scrapy
import requests
from bs4 import BeautifulSoup
import re
import random
import time
#import os
#path = os.path.abspath(os.path.join(os.getcwd(),"../.."))
#import sys
#sys.path.append(path)
from liepin.items import LiepinItem
#import main

User_Agent = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/74.0.3729.157 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.8.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/74.0.3729.157 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.8.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.2.5 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94'
]

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'_uuid=72C80342FFA84819742958C7A0B64A7C; __uuid=1560998873354.38; gr_user_id=975cc25f-4e87-408a-a617-cd6c64168f81; bad1b2d9162fab1f80dde1897f7a2972_gr_last_sent_cs1=28e8da9e4881dfab1a667e00ad0d9493; grwng_uid=fd3a3c95-9993-4b27-a7b1-2ab9b321f2bd; need_bind_tel=false; c_flag=9d3c4fb22bb5dac5f60faa6c32b446f4; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1561428135,1561527854,1561686690,1561795135; _mscid=00000000; abtest=0; char_captcha=AD6461E7C0A84806399202FA0E3CE171; user_roles=0; new_user=false; fe_se=-1561983188600; fe_all_localcookie_sessionid=34599-35245-1561983217450; fe_im_socketSequence_0=8_4_4; bad1b2d9162fab1f80dde1897f7a2972_gr_cs1=28e8da9e4881dfab1a667e00ad0d9493; _fecdn_=1; __tlog=1561795133892.69%7C00000000%7CR000000075%7C00000000%7C00000000; JSESSIONID=CCE2781F9A049173262B936D8C13A537; __session_seq=63; __uv_seq=13; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1562124621',
'DNT':'1',
'Host':'www.liepin.com',
'Upgrade-Insecure-Requests':'1'
#'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/67.0'
}

class LiepinSpider(scrapy.Spider):
    name = 'liepin'
    url0 = 'https://www.liepin.com'
    url1 = 'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=020&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=python&init=-1&searchType=1&headckid=e685f3c49cd5e997&compkind=&fromSearchBtn=2&sortFlag=15&ckid=e685f3c49cd5e997&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=I-7rQ0e90mv8a37po7dV3Q~r3i1HcfrfE3VRWBaGW6LoA&d_sfrom=search_prime&d_ckId=3a692788a83669c4ae2fd45d875169fd&d_curPage=0&d_pageSize=40&d_headId=3a692788a83669c4ae2fd45d875169fd&curPage='
#   'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=020&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=python+%E6%95%B0%E6%8D%AE&init=-1&searchType=1&headckid=3a01c1305fbdb82d&compkind=&fromSearchBtn=2&sortFlag=15&ckid=3a01c1305fbdb82d&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=OtDZYln6raiWh2NGqeOwFg~r3i1HcfrfE3VRWBaGW6LoA&d_sfrom=search_prime&d_ckId=71fbc11396ad17db29c7d234740c86b1&d_curPage=99&d_pageSize=40&d_headId=71fbc11396ad17db29c7d234740c86b1&curPage='
    page = 0
    page_max = 1
   
    def parse(self,response):
        item = LiepinItem()
#        self.logger.warning('details:',response.url)
#        from scrapy.shell import inspect_response
#        inspect_response(response,self)                ##debug 
        job_list = response.css('ul.sojob-list') ## response.xpath('//ul[@class="sojob-list"]')
        for i in range(1,4):
            positionName = job_list.css('li:nth-child({}) h3 a::text'.format(str(i))).extract()
            positionFrom = job_list.css('li:nth-child({}) i.icon b::text'.format(str(i))).extract()
            salary = job_list.css('li:nth-child({}) p.condition span.text-warning::text'.format(str(i))).extract()
            city = job_list.css('li:nth-child({}) p.condition a::text'.format(str(i))).extract()
            education = job_list.css('li:nth-child({}) p.condition span.edu::text'.format(str(i))).extract()
            workYear = job_list.css('li:nth-child({}) p.condition span:last-child::text'.format(str(i))).extract()
            update_time= job_list.css('li:nth-child({}) p.time-info time::text'.format(str(i))).extract()
            companyName = job_list.css('li:nth-child({}) p.company-name a::text'.format(str(i))).extract()
            companyLink = job_list.css('li:nth-child({}) p.company-name a::attr(href)'.format(str(i))).extract()
            industryField = job_list.css('li:nth-child({}) p.field-financing span::text'.format(str(i))).extract()
            positionLink = job_list.css('li:nth-child({}) h3 a::attr(href)'.format(str(i))).extract()
            positionDescription = ['']
            companySize = ['']
            
            item['positionName'] = ''.join(positionName).strip()
            item['positionFrom'] = ''.join(positionFrom)
            item['salary'] = ''.join(salary)
            item['city'] = ''.join(city)
            item['education'] = ''.join(education)
            item['workYear'] = ''.join(workYear)
            item['update_time'] = ''.join(update_time)
            item['companyName'] = ''.join(companyName)
            item['companyLink'] = ''.join(companyLink)
            item['industryField'] = ''.join(industryField).strip()
            item['positionLink'] = ''.join(positionLink)
            item['positionDescription'] = ''.join(positionDescription)
            item['companySize'] = ''.join(companySize)
            
            if (item['positionFrom'] == '猎'):
                item['positionLink'] = self.url0 + item['positionLink']
                item['companyLink'] = '猎'
            
            link = item['positionLink']
            item['positionDescription'] = self.get_data(link)
            
            yield item


        print("正在处理第{}页,请耐心等待...".format(self.page))
        
        if (self.page < self.page_max):
            self.page += 1
            ua = random.choice(User_Agent)
            headers['User_Agent'] = ua
            next_link = self.url1 + str(self.page)
#            time.sleep(1)
            yield scrapy.http.Request(url=next_link,headers=headers,callback=self.parse)
            
    def get_data(self,link):
        time.sleep(1)
        ua = random.choice(User_Agent)
        headers['User_agent'] = ua
        html = requests.get(link,headers=headers).text
        soup = BeautifulSoup(html,'lxml') #,from_encoding='utf-8'
        data = soup.select("div.job-description div.content")
        tags = data[0]
        text = tags.text
        return text

    def start_requests(self):
        start_url = self.url1 + str(self.page)
        ua = random.choice(User_Agent)
        headers['User-Agent'] = ua
        return [scrapy.http.Request(url=start_url,headers=headers,callback=self.parse)]