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




zang_weibo_generator = DocGenerator(2011, 
                                    'weibo_zang.json',
                                    '../微博文档/藏微博/')
                                    
                                    
zang_weibo_generator.generateDoc()
                  


han_weibo_generator = DocGenerator(2010, 
                                    'weibo_han.json',
                                    '../微博文档/汉微博/')
                                    
                                    
han_weibo_generator.generateDoc()       

                           