# coding:utf-8

"""
    python 操作word
"""
import json

import os
import sys
import re
import datetime
import time


weibofile="./JsonData/weibo_all.json"

with open(weibofile,'r',encoding='utf-8') as f:
    weibo_all = json.load(f)
        
currentYear = 2020

for i in range(0, len(weibo_all)):
    weibo = weibo_all[i]
    if not re.search(r"[0-9][0-9][0-9][0-9]", weibo['date']):
        struct_time = time.strptime('2020年'+weibo['date'], "%Y年%m月%d日 %H:%M")
        weibo['date'] = time.strftime("%Y-%m-%d %H:%M", struct_time)
    else:
        struct_time = time.strptime(weibo['date'], "%Y-%m-%d %H:%M")
        weibo['date'] = time.strftime("%Y-%m-%d %H:%M", struct_time)

    weibo_all[i] = weibo
    

ouputfile = './JsonData/weibo_all_new.json'
with open(ouputfile,'w',encoding='utf-8') as file_obj:
    json.dump(weibo_all,file_obj,indent=4,ensure_ascii=False)



if __name__ == "__main__":
    pass
