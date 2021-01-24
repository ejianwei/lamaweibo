# coding:utf-8

"""
    python 操作word
"""
import json

import os
import sys
import re
import datetime


picDir = "./Image/"


class DocGenerator:
 
    def __init__(self,startYear, weibofile,docDir):

        self.startYear = startYear
        self.weibofile = weibofile
        self.docDir = docDir

    def generateDoc(self):

        with open(self.weibofile,'r',encoding='utf-8') as f:
            weibo_all = json.load(f)
                
        currentYear = datetime.datetime.now().year
        weibo_by_year = {}

        #把微博数据按年分组，每年的微博是一个list
        for i in range(int(self.startYear), currentYear+1):
            weibo_by_year[str(i)] = []

        for weibo in weibo_all:
            weibo_by_year[weibo['date'][0:4]].insert(0,weibo)

        #每一年的微博，生成一个markdown文件        
        for year in range(self.startYear, currentYear+1):
            
            weibo_data = weibo_by_year[str(year)]

            mdfile = self.docDir + 'weibo'+str(year)+'.md'
            fo = open(mdfile, "w",encoding='utf-8')
            print ("生成文档：%s" % mdfile)
            
            for weibo_item in weibo_data:

                weibodate = weibo_item['date']
                weibotext = weibo_item['text']

                fo.write( " ## ")
                fo.write( weibodate)
                fo.write("\n")

                fo.write(weibotext)
                fo.write("\n")

                if 'note' in weibo_item:
                    fo.write( "( ")
                    fo.write(weibo_item['note'])
                    fo.write( " )")
                    fo.write("\n")
                    
                if 'external' in weibo_item:
                
                    if 'mark' in weibo_item['external']:

                        fo.write( " > ")
                        fo.write( weibo_item['external']['mark'])
                        fo.write("\n")
                    else:
                        fo.write( " > ")
                        fo.write( weibo_item['external']['author'])
                        fo.write("\n")
                    
                        fo.write( " > ")
                        fo.write( weibo_item['external']['text'])
                        fo.write("\n")
                        
                        if 'images' in weibo_item['external']:
                            #遍历图片
                            for weibo_image in weibo_item['external']['images']:
                                picfile = picDir + str(weibo_image)
                                imgstr = '<img src="' + picfile + '" width="400">'
                                fo.write( imgstr)
                            fo.write("\n")
                elif 'images' in weibo_item:
                    #遍历图片
                    for weibo_image in weibo_item['images']:
                        picfile = picDir + str(weibo_image)

                        imgstr = '<img src="' + picfile + '" width="400">'
                        fo.write( imgstr)
                    fo.write("\n")
            # 关闭打开的文件
            fo.close()

