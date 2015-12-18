#!/usr/bin/python
# coding:utf-8

import re
import urllib2
import urllib
import socket
import os
import sys
from multiprocessing import Pool
import threading
import time

def parse_url(s):
    dic = {
        "0": "7", "1": "d", "2": "g", "3": "j", "4": "m", "5": "o", "6": "r", "7": "u", "8": "1",
        "9": "4", "a": "0", "b": "8", "c": "5", "d": "2", "e": "v", "f": "s", "g": "n", "h": "k",
        "i": "h", "j": "e", "k": "b", "l": "9", "m": "6", "n": "3", "o": "w", "p": "t", "q": "q",
        "r": "p", "s": "l", "t": "i", "u": "f", "v": "c", "w": "a"
    }
    s = s.replace("AzdH3F", "/")
    s = s.replace("_z2C$q", ":")
    s = s.replace("_z&e3B", ".")
    p = ""
    for i in s:
        if i in dic.keys():
            p += dic[i]
        else:
            p += i

    return p

def imgs_retrieve(result, page, i, imgs_per_page, pre_name):
    real_url = parse_url(result)
    # real_url = result
    # print real_url
    pic_name = "%s_%s_%s.jpg" % (pre_name, str(page),  str(i) )
    print 'downloading pic No.%s' % str(i+(page-1)*imgs_per_page)

    dirname = '_'.join([pre_name, str((page-1)/10*10+1),str(((page-1)/10+1)*10)])

    if not os.path.exists(dirname):
        os.mkdir(dirname)
    name = dirname+'/%s' % pic_name
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


#def baidu_crawler(start, word, ren):
def baidu_crawler(task):
    imgs_per_page = 60
    page = task[0]
    start = (page-1)*imgs_per_page
    end = (page)*imgs_per_page
    word = task[1]
    # json_url = '''http://image.baidu.com/search/acjson?tn=resultjson_com&ie=utf-8&pn=%s&word=%s&rn=%s&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1#'''
    json_url = '''http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%s&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=ala&pn=%s&rn=%s&gsm=3c&1450340113203#'''
    key_word = []
    for item in word:
        a = urllib.quote(item)
        key_word.append(a)

    key_word_string = '+'.join(key_word)
    pre_name = '_'.join(word)

    url = json_url % (key_word_string, key_word_string, str(start), str(end))
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
    pattern_url = re.compile(r'\"objURL\":\"(.*?)\",', re.S)
    result_pic = pattern_url.findall(content)

    i = 0
    threads = []
    for result in result_pic:
        t = threading.Thread(target=imgs_retrieve, args=(result, page, i, imgs_per_page, pre_name,))
        t.start()
        threads.append(t)
        i = i+1
        time.sleep(0.2)
    for t in threads:
        t.join()


        # real_url = parse_url(result)
        # # real_url = result
        # # print real_url
        # i += 1
        # pic_name = "%s_%s_%s.jpg" % (pre_name, str(page),  str(i) )
        # print 'downloading pic No.%s' % str(i+(page-1)*imgs_per_page)

        # dirname = '_'.join([pre_name, str(page/10*10+1),str((page/10+1)*10)])

        # if not os.path.exists(dirname):
            # os.mkdir(dirname)
        # name = dirname+'/%s' % pic_name
        # if os.path.isfile(name):
            # os.remove(name)
        # try:
            # socket.setdefaulttimeout(20)
            # urllib.urlretrieve(real_url, name)
        # except urllib.ContentTooShortError, e:
            # print 'error 1'
            # print e
            # os.remove(name)
        # except socket.timeout, e:
            # print 'error 2'
            # print e
            # os.remove(name)
        # except IOError, e:
            # print 'error 3'
            # print e
            # # f = open(name%str(i),'w+')
            # # f.write(content)
            # # f.close()

def my_crawler(sp, ep, word):
    # multiprocessing implenmention
    pool = Pool(4)
    task = [(x, word) for x in range(sp, ep+1)]
    #print task
    pool.map(baidu_crawler,task)
    pool.close()
    pool.join()


if __name__ == '__main__':

    args = sys.argv
    if len(args) < 4:
        print u'参数格式错误'
        print u'格式：python baidu_crawler.py start_page end_page word\nstart_num:开始页码\nend_num:结束页码\nword:关键字(关键字可以用空格隔开)'
        sys.exit(0)
    start_page= int(args[1])
    end_page= int(args[2])
    word = args[3:]

    my_crawler(start_page, end_page, word)
