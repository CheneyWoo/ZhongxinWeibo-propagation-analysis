#!/usr/bin/python
#coding=utf-8

import urllib2
import csv
import time
import json
import re
import requests
from bs4 import BeautifulSoup
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

myheader1 = {
    'cookie': '_T_WM=ab2659dc3d6dc49b941dfd4603194652; ALF=1537681408; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW2JQe9LinWeoVqTw8dpugC5JpX5K-hUgL.Fozcehe0So27SoM2dJLoI7DhIsHV9PLPdcva; MLOGIN=1; SUHB=0M2EEWKWuBg39i; SSOLoginState=1535089434',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

myheader2 = {
    'cookie': '_T_WM=ab2659dc3d6dc49b941dfd4603194652; ALF=1538048715; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW2JQe9LinWeoVqTw8dpugC5JpX5K-hUgL.Fozcehe0So27SoM2dJLoI7DhIsHV9PLPdcva; SUHB=0U1IKs3b8Cvw7E; SSOLoginState=1535509073; MLOGIN=1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

base_url1 = 'https://m.weibo.cn/api/statuses/repostTimeline?id={ids}&page={numbers}'
base_url2 = 'https://m.weibo.cn/api/statuses/repostTimeline?id={ids}&page={numbers}'

user_url = 'https://m.weibo.cn/status/{mids}?display=0&retcode=6102'

file = open('xiaoyemeizi.csv', 'a+')
writer = csv.writer(file)

usercount = 0
def get_page(url):
    request = urllib2.Request(url, headers=myheader2)
    html = urllib2.urlopen(request).read()
    return html
    #jsonpage = json.loads(html.encode('utf-8'))
    #return jsonpage

def get_repostuser_info(id,l,r,level = 1):
    for number in range(l,r):
        #time.sleep(0.5)
        url = base_url2.format(ids = id,numbers = number)
        page = get_page(url)
        page = json.loads(page.encode('utf-8'))
        for i in range(0,len(page['data']['data'])):
            data = []
            user_name = page['data']['data'][i]['user']['screen_name']
            followers_count = page['data']['data'][i]['user']['followers_count']
            reposts_count = page['data']['data'][i]['reposts_count']
            date = page['data']['data'][i]['created_at']
            text = page['data']['data'][i]['text']
            mid = page['data']['data'][i]['mid']

            data.append(user_name)
            data.append(followers_count)
            data.append(date)
            data.append(reposts_count)
            data.append(level)

            friends = re.findall("(?<=>@).*?(?=<)", text)
            data.append(len(friends))
            for friend in friends:
                data.append('@' + str(friend))
            writer.writerow(data)

            if reposts_count > 0 and mid!=id:
                get_repostuser_info(mid, 1, 2, level = level + 1)

            print user_name, followers_count, date, len(friends), reposts_count, level
        #print "page" + str(number) + " over"

#get_repostuser_info(4253051688686091,1,1004,1)
get_repostuser_info(4273989696658059,1,61,1)
file.close()