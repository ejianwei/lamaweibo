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


def cbk(a,b,c):  
    '''''回调函数 
    @a:已经下载的数据块 
    @b:数据块的大小 
    @c:远程文件的大小 
    '''  
    per=100.0*a*b/c  
    if per>100:  
        per=100  
    print('%.2f%%' % per)
    
def formatWeiboDate(weiboDate):

    currentYear = datetime.datetime.now().year
  
    if not re.search(r"[0-9][0-9][0-9][0-9]", weiboDate):
        struct_time = time.strptime(str(currentYear)+'年'+weiboDate, "%Y年%m月%d日 %H:%M")
    else:
        struct_time = time.strptime(weiboDate, "%Y-%m-%d %H:%M")
        
    formatDate = time.strftime("%Y-%m-%d %H:%M", struct_time)

    return formatDate
    
    
def isElementExist(x,element):
    flag=True
   
    try:
        x.find_element_by_css_selector(element)
        return flag
    
    except:
        flag=False
        return flag

def getImage(image_link, filepath):
    if image_link == "https://p4.ivideo.sina.com.cn/screenshot/17268237_3.jpg" or \
       image_link == "https://v140.56img.com/images/16/19/r307933440i56olo56i56.com_138200515099hd.jpg" or \
       image_link == "https://r3.sinaimg.cn/201501/120/120/aHR0cDovL21tYml6LnFwaWMuY24vbW1iaXovVXd3T1hGR1J6Q25LRVRJMUx4UUtrNWZyenRLakh3MWNVelJuYnd3c216V0h1cW9BSjZENUhhZGRIWmliT2hOTXNpYXFFOW5ZaklLWmhHUGljd0lnUk5aelEvMCtodHRwOi8vbXAud2VpeGluLnFxLmNvbS9zP19fYml6PU16QTNPRGM1T1RReU5BPT0mbWlkPTIwMjgzODM3NCZpZHg9MSZzbj01OTc3NDg0NjQyNzg5YjcyMjgwODNjOWIxZjA2NmIzMyZzY2VuZT0xJmtleT0yZjVlYjAxMjM4ZTg0ZjdlYWM1NDE5NzA1YzE2NGE2NDYxY2U2MmQ2YzJiN2ZlZWRiZDM3YmViMjk3NzE0NmVjYTYzODhmOTU5MGQ3ZDk4OWM3YzBkZTQyMzI2YWY1NWImYXNjZW5lPTEmdWluPU1UVXdNamMzT1RNeU1RJTNEJTNEJmRldmljZXR5cGU9d2Vid3gmdmVyc2lvbj03MDAwMDAwMSZwYXNzX3RpY2tldD1iWGhGTXFvTEs5ckJiNE9ZVEslMkZzNlIwSTVscDJCSWZ1eEs2MVUzSFp4dUdsYyUyRjNoZnBhVndDcUY2MDZsMXdtSg==.jpg" or \
       image_link == "https://r3.sinaimg.cn/201507/120/120/aHR0cDovL21tYml6LnFwaWMuY24vbW1iaXovVXd3T1hGR1J6Q2xRM3BSN0RXWEZaVlF3Tm4zS280TExCZ0tLbnJzUEtSVjhSRG1pYm9KT3d2S1duRnBhM2lhNDVYekptOG1DOFhRcmpWc3hWdGppYmRLM1EvMD93eF9mbXQ9anBlZytodHRwOi8vbXAud2VpeGluLnFxLmNvbS9zP19fYml6PU16QTNPRGM1T1RReU5BPT0mbWlkPTIwODIxNTk5MiZpZHg9MSZzbj1iMzMzOWI4OTEwNzI4NGM2MGU2ZWVhOGU4ZGY2ZDFlNiYzcmQ9TXpBM01EVTROVFl6TXc9PSZzY2VuZT02.jpg" or \
       image_link == "https://r3.sinaimg.cn/201509/120/120/aHR0cDovL21tYml6LnFwaWMuY24vbW1iaXovNjBNOEd0THNpYnFlOVhBWXRXMlFqYUxVbnE4QjY4akppY1kwS2g0aWJUT1JBTjJXMUUyc0hVN0JCelU2Y0RDcDJQQTJzYTJLNjhDa3dsUzU1Um1ZNkZQaWNRLzA/d3hfZm10PWpwZWcraHR0cDovL21wLndlaXhpbi5xcS5jb20vcz9fX2Jpej1NekEzTmpFeE5qZzBPQT09Jm1pZD0yMjI0NTc5NjYmaWR4PTEmc249N2I4YTNmZGY3NGViZDU2Y2ZiMWFjY2M5NGMwYTkwYWMmc2NlbmU9MSZzcmNpZD0wOTI4MXU5Tkd1WW01Wm1YSVdseG1HbjIma2V5PTI4NzdkMjRmNTFmYTUzODRjZjcyNGUwZjg5OWE2MDNkNzAzMTlkYjQ2YjgyYjUwOGZiYWI1MjYyMTMyNzEyY2I5OTg3MTc3NDIzNDNmMDgyNTdhYjMxMmI1MjQyZGVlNyZhc2NlbmU9MSZ1aW49TVRVd01qYzNPVE15TVElM0QlM0QmZGV2aWNldHlwZT1XaW5kb3dzKzgmdmVyc2lvbj02MTA1MDAxNiZwYXNzX3RpY2tldD1sblRGU0QzbTZKN3JpbnF3U0E3dkFwNm0lMkZGT2x6Z0RNWnExbHBURjJEaUJyMUhqWlZXJTJCMjhxblh0UzA5Z1o5JTJC.jpg": 
        
        
        print ("该图片不存在，跳过处理")
        return False
    else:
        print("downloadeding " + image_link)
        urlretrieve(image_link,filepath)
        return True
                
def getExternalWB(weibo_detail):
    weibo_item_json = {}
    
    
    if weibo_detail.text.find("抱歉，此微博已被作者删除") != -1 or \
       weibo_detail.text.find("抱歉，由于作者设置，你暂时没有这条微博的查看权限哦") != -1  or \
       weibo_detail.text.find("抱歉，作者已设置仅展示半年内微博，此微博已不可见") != -1  or \
       weibo_detail.text.find("该账号行为异常，存在安全风险，用户验证之前暂时不能查看") != -1  or \
       weibo_detail.text.find("该账号内容存在风险，用户验证之前暂时不能查看。") != -1  or \
       weibo_detail.text.find("该账号因被投诉违反法律法规和《微博社区公约》的相关规定") != -1  or \
       weibo_detail.text.find("该账号因被投诉违反《微博社区公约》的相关规定，现已无法查看。") != -1:
        print("转发的微博已被删除")
        weibo_item_json['mark'] = "转发的微博已被删除"
    else:
            
        
        #获取作者
        weibo_info_item = weibo_detail.find_element_by_css_selector('.WB_info')
        weibo_item_json['author'] = weibo_info_item.find_element_by_tag_name('a').text

            
        #获取文字
        weibo_text_item = weibo_detail.find_element_by_css_selector('.WB_text')

        weibo_item_json["text"] = weibo_text_item.text
        
        if weibo_item_json["text"].find("展开全文") != -1:
        
            #expand_item = weibo_text_item.find_element_by_tag_name('a')
            expand_item = weibo_text_item.find_element_by_css_selector('.W_ficon.ficon_arrow_down')
            ActionChains(x).move_to_element(weibo_text_item).click(expand_item).perform()
                        
            time.sleep(1)
            weibo_text_items = weibo_detail.find_elements_by_css_selector('.WB_text')
            weibo_item_json["text"] = weibo_text_items[1].text
            weibo_item_json["text"] = re.sub(r'收起全文.*$', "", weibo_item_json["text"])

        print (weibo_item_json["text"])

        
        #获取图片
        if isElementExist(weibo_detail,'.WB_media_wrap.clearfix' ):

            weibo_media_wrap = weibo_detail.find_element_by_css_selector('.WB_media_wrap.clearfix')
            
            images = weibo_detail.find_elements_by_tag_name('img')
            
            weibo_item_json["images"] = []
            weibo_item_json["imagesURL"] = []
            
            for image in images:
                image_link = image.get_attribute('src')
                image_link = image_link.replace("/orj360/", "/large/");
                image_link = image_link.replace("/thumb150/", "/large/");
                #print("image link:")
                #print(image_link)
                
                #去掉/之前的前缀
                filename = re.sub(r'^.*/', "", image_link)
                filename = re.sub(r'\?.*$', "", filename)
                
    #            if re.search(r"\?", filename):
    #                print("this is a video! continue!")
    #                continue

                #print ("file name")
                #print (filename)
                
                filepath = ".\\Image\\" + filename
               
               

                if getImage(image_link,filepath):
                #time.sleep(1)
                    weibo_item_json["images"].append(filename)
                    weibo_item_json["imagesURL"].append(image_link)
                
                
    return weibo_item_json

#主逻辑     
#加载chrome driver  
x = webdriver.Chrome(r'.\chromedriver.exe') 

cookiefile = './weibo_cookies.json'

#加载微博数据文件
weibofile="./JsonData/weibo_all.json"
#先备份
copyfile(weibofile, "./JsonData/weibo_all.bak.json")

with open(weibofile,'r',encoding='utf-8') as f:
    weibo_all = json.load(f)
    
    
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
    #首次登陆多等一会
    
weibo_json = []

syncFinished = False
#按页浏览微博
for page_num in range(1, 9999):

    if syncFinished:
        print ("同步完成")
        break
    print ("Open page " + str(page_num))
    
    page_url = 'https://weibo.com/sdjzwh?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page='
    
    page_url = page_url + str(page_num)
    page_url = page_url + '#feedtop'
    
    
    x.get(page_url)

    print ("sleep 15s!")
    #留十秒页面加载时间
    time.sleep(10)


    #下拉两次，到页面底部，每次留3s页面加载时间

    print ("Scrolling!")
    js="var q=document.documentElement.scrollTop=100000"  
    x.execute_script(js)  
    time.sleep(3)  
        
        
    print ("Scrolling!")
    js="var q=document.documentElement.scrollTop=200000"  
    x.execute_script(js)  
    time.sleep(3)  
        
    print ("Scrolling!")
    js="var q=document.documentElement.scrollTop=300000"  
    x.execute_script(js)  
    time.sleep(3)  
    
    

    #获取全部微博
    weibo_details = x.find_elements_by_css_selector('.WB_detail')

    #遍历每一条微博
    for weibo_detail in weibo_details:


        
        weibo_item_json = {}
        
        #跳过不是本账号的微博(点赞的微博)
        weibo_info_item = weibo_detail.find_element_by_css_selector('.WB_info')
        if weibo_info_item.find_element_by_tag_name('a').text.find("索达吉藏文化") == -1:
            continue

        #获取日期
        weibo_from_item = weibo_detail.find_element_by_css_selector('.WB_from.S_txt2')
        weibo_date = weibo_from_item.find_element_by_tag_name('a').text
        
        #处理日期，转化为yyyy-mm-dd的格式
        weibo_item_json["date"] = formatWeiboDate(weibo_date)
        print (weibo_item_json["date"])
        
        if weibo_item_json["date"] == weibo_all[0]["date"]:
            print("更新到上一次同步位置！")
            syncFinished = True
            break
            
        weibo_text_item = weibo_detail.find_element_by_css_selector('.WB_text.W_f14')
        
        #获取文字
        weibo_item_json["text"] = weibo_text_item.text
        
        if weibo_item_json["text"].find("展开全文") != -1:
        
            specialDate = ['2019-10-1 05:22','2019-9-29 14:21', '2019-9-26 21:20', '2019-9-13 09:41', '2019-9-9 23:12', '2019-9-7 05:20', '2019-8-23 05:35' ]
            #特殊处理
            if weibo_item_json["date"] in  specialDate:
                weibo_item_json["note"] = "注：无法获取本条完整微博"
                print("!!!!!!!!! skip expanding !!!!!! for " + weibo_item_json["date"])
            else:
                #expand_item = weibo_text_item.find_element_by_tag_name('a')
                expand_item = weibo_text_item.find_element_by_css_selector('.W_ficon.ficon_arrow_down')
                ActionChains(x).move_to_element(weibo_text_item).click(expand_item).perform()
                            
                time.sleep(3)
                weibo_text_items = weibo_detail.find_elements_by_css_selector('.WB_text.W_f14')
                weibo_item_json["text"] = weibo_text_items[1].text
                weibo_item_json["text"] = re.sub(r'收起全文.*$', "", weibo_item_json["text"])
        
        print (weibo_item_json["text"])
    
        #如果存在转发的微博
        if isElementExist(weibo_detail,'.WB_feed_expand' ):
            weibo_item_json["external"] = getExternalWB(weibo_detail.find_element_by_css_selector('.WB_feed_expand'))
        
        #获取图片
        if isElementExist(weibo_detail,'.WB_media_wrap.clearfix' ):

            weibo_media_wrap = weibo_detail.find_element_by_css_selector('.WB_media_wrap.clearfix')
            
            images = weibo_detail.find_elements_by_tag_name('img')
            
            weibo_item_json["images"] = []
            weibo_item_json["imagesURL"] = []
            for image in images:
                image_link = image.get_attribute('src')
                image_link = image_link.replace("/orj360/", "/large/");
                image_link = image_link.replace("/thumb150/", "/large/");
                #print("image link:")
                #print(image_link)
                
                #去掉/之前的前缀
                filename = re.sub(r'^.*/', "", image_link)
                filename = re.sub(r'\?.*$', "", filename)

                #print ("file name")
                #print (filename)
                
                filepath = ".\\Image\\" + filename
               

                
                if getImage(image_link,filepath):
                    weibo_item_json["images"].append(filename)
                    weibo_item_json["imagesURL"].append(image_link)
                
            
        weibo_json.append(weibo_item_json)


weibo_json = weibo_json + weibo_all
#保存文件
with open(weibofile,'w',encoding='utf-8') as file_obj:
    json.dump(weibo_json,file_obj,indent=4,ensure_ascii=False)

print ('数据文件存储完成!!!')

#print ("start click next page!!!!!!")
#nextPageButton = x.find_element_by_css_selector('.page.next.S_txt1.S_line1')
##nextPageButton = x.find_element_by_class_name('next')
##nextPageButton.click()
#
#print(nextPageButton.text)
#
#Action = ActionChains(x)
#
#Action.move_to_element(nextPageButton).click().perform()
#
#time.sleep(3)  
#Action.move_to_element(nextPageButton).click().perform()

#x.close()