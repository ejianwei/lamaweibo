#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import re
import os  
from urllib.request import urlretrieve

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import datetime
from shutil import copyfile

from weiboDownloader import Downloader
from weiboDocGenerator import DocGenerator

cookiefile = './weibo_cookies.json'
    
x = webdriver.Chrome(r'.\chromedriver.exe') 

#登陆账号
if not os.path.exists(cookiefile):
    print ("cookies not exists!")
    #进入微博主页
    x.get('https://weibo.com/')
    
    #留给登录操作时间
    print ("sleep 60s!")
    time.sleep(60)
    
    print ("saving cookies!")
    cookies = x.get_cookies()

    with open(cookiefile,'w',encoding='utf-8') as file_obj:
        json.dump(cookies,file_obj,indent=4,ensure_ascii=False)

else:

    print("loading cookies")
    with open(cookiefile,'r',encoding='utf-8') as f:
        cookies = json.load(f)
    
    x.get('https://weibo.com/')
    for cookie in cookies:
        x.add_cookie(cookie)

    #留给登录操作时间
    print ("sleep 60s!")
    time.sleep(60)
#更新藏微博
print("更新藏微博")
zang_downloader = Downloader(x, 
                            'https://weibo.com/sdjzwh?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=',
                            "索达吉藏文化",
                            ['2019-10-1 05:22','2019-9-29 14:21', '2019-9-26 21:20', '2019-9-13 09:41', '2019-9-9 23:12', '2019-9-7 05:20', '2019-8-23 05:35' ],
                            'weibo_zang.json',
                            '../微博文档/藏微博/Image/')
                            
zang_downloader.download()                            

zang_weibo_generator = DocGenerator(2011, 
                                    'weibo_zang.json',
                                    '../微博文档/藏微博/')
                                    
                                    
zang_weibo_generator.generateDoc()
                  
#更新汉微博                  
print("更新汉微博")
han_downloader = Downloader(x, 
                            'https://weibo.com/suodj?pids=Pl_Official_MyProfileFeed__21&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=',
                            "索达吉堪布",
                            ['2019-09-11 05:05','2019-09-29 05:19'],
                            'weibo_han.json',
                            '../微博文档/汉微博/Image/')
                            
han_downloader.download()   

han_weibo_generator = DocGenerator(2010, 
                                    'weibo_han.json',
                                    '../微博文档/汉微博/')
                                    
                                    
han_weibo_generator.generateDoc()       

                           