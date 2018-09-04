#!/usr/bin/python
#coding=utf-8

import urllib2
import csv
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

myheader1 = {
    'cookie': '_T_WM=ab2659dc3d6dc49b941dfd4603194652; ALF=1537681408; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW2JQe9LinWeoVqTw8dpugC5JpX5K-hUgL.Fozcehe0So27SoM2dJLoI7DhIsHV9PLPdcva; MLOGIN=1; SUHB=0M2EEWKWuBg39i; SSOLoginState=1535089434',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

base_url1 = 'https://m.weibo.cn/api/container/getIndex?containerid=2304131907753765_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={numbers}'

file = open('minshengyinhang.csv', 'a+')
writer = csv.writer(file)

def get_page(url):
    request = urllib2.Request(url, headers=myheader1)
    html = urllib2.urlopen(request).read()
    return html
    #jsonpage = json.loads(html.encode('utf-8'))
    #return jsonpage

def get_weibo_info(l,r):
    for number in range(l,r):
        url = base_url1.format(numbers = number)
        page = get_page(url)
        page = json.loads(page.encode('utf-8'))
        for i in range(0, len(page['data']['cards'])):
            data = []
            attitudes_count = page['data']['cards'][i]['mblog']['attitudes_count']
            comments_count = page['data']['cards'][i]['mblog']['comments_count']
            reposts_count = page['data']['cards'][i]['mblog']['reposts_count']
            created_at = page['data']['cards'][i]['mblog']['created_at']

            data.append(attitudes_count)
            data.append(comments_count)
            data.append(reposts_count)
            data.append(created_at)

            writer.writerow(data)

        print attitudes_count, comments_count, reposts_count, created_at

get_weibo_info(61,65)
file.close()