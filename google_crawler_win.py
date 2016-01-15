#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2
import urllib
import socket
import os
import sys
from multiprocessing import Pool
import threading
import time


def imgs_retrieve(result, page, i, imgs_per_page, pre_name):
    real_url = result
    pic_name = "%s_%s_%s.jpg" % (pre_name, str(page), str(i))
    #保证名称编码是GBK
    pic_name = pic_name.decode('gbk')
    print 'downloading pic No.%s' % str(i + (page - 1) * imgs_per_page)

    dirname = '_'.join([pre_name, str((page - 1) / 10 * 10 + 1), str(((page - 1) / 10 + 1) * 10)])

    #保证目录名称编码是GBK
    dirname = dirname.decode('gbk')
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    name = dirname + '/%s' % pic_name
    if os.path.isfile(name):
        os.remove(name)
    try:
        socket.setdefaulttimeout(10)
        urllib.urlretrieve(real_url, name)
    except urllib.ContentTooShortError, e:
        print 'error 1'
        print e
        os.remove(name)
    except socket.timeout, e:
        print 'error 2'
        print e
        os.remove(name)
    except IOError, e:
        print 'error 3'
        print e


def crawler(task):
    imgs_per_page = 100
    page = task[0]
    start = (page - 1) * imgs_per_page
    end = (page) * imgs_per_page
    word = task[1]
    # json_url = '''http://image.baidu.com/search/acjson?tn=resultjson_com&ie=utf-8&pn=%s&word=%s&rn=%s&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1#'''
    # json_url = '''http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%s&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=ala&pn=%s&rn=%s&gsm=3c&1450340113203#'''
    json_url = '''https://www.google.com/search?newwindow=1&hl=en&authuser=0&site=imghp&tbm=isch&source=hp&biw=1214&bih=705&q=%s&oq=%s&start=%s&end=%s&ei=vPaYVsphysqPA7yJo7AB&ved=0ahUKEwjKr_nW-KvKAhVK5WMKHbzECBYQuT0IJCgB&vet=10ahUKEwjKr_nW-KvKAhVK5WMKHbzECBYQuT0IJCgB.vPaYVsphysqPA7yJo7AB.i&ijn=%s'''
    key_word = []
    for item in word:
        #保证编码为utf-8
        a = urllib.quote(item.decode('gbk').encode('utf-8'))
        key_word.append(a)

    key_word_string = '+'.join(key_word)
    pre_name = '_'.join(word)

    url = json_url % (key_word_string, key_word_string, str(start), str(end),str(page))
    print url

    headers = {'Accept': 'image/webp',
               'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36''',}
    req = urllib2.Request(url, headers=headers)
    try:
        content = urllib2.urlopen(req).read()
    except urllib2.URLError, e:
        print e
    # f = open('a.txt','w+')
    # f.write(content)
    # f.close()
    pattern_url = re.compile(r'imgurl=(.*?)&amp;', re.S)
    result_pic = pattern_url.findall(content)

    for i,temp in enumerate(result_pic):
        if temp.find('$') <> -1:
            result_pic[i] = temp[:temp.find('$')]

    i = 1
    threads = []
    for result in result_pic:
        t = threading.Thread(target=imgs_retrieve, args=(result, page, i, imgs_per_page, pre_name,))
        t.start()
        threads.append(t)
        i += 1
        time.sleep(0.2)
    for t in threads:
        t.join()


def my_crawler(sp, ep, w):
    # multiprocessing implenmention
    pool = Pool(4)
    task = [(x, w) for x in range(sp, ep + 1)]
    # print task
    pool.map(crawler, task)
    pool.close()
    pool.join()


if __name__ == '__main__':

    args = sys.argv
    if len(args) < 4:
        print u'参数格式错误'
        print u'格式：python baidu_crawler.py start_page end_page word\nstart_num:开始页码\nend_num:结束页码\nword:关键字(关键字可以用空格隔开)'
        sys.exit(0)
    start_page = int(args[1])
    end_page = int(args[2])
    if start_page > end_page:
        print u'页码错误'
        sys.exit(0)
    word = args[3:]

    my_crawler(start_page, end_page, word)
