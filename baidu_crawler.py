# coding:utf-8

import re
import urllib2
import urllib
import datetime
import socket
import os
import sys


# from threading import Thread



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


def baidu_crawler(start, word, ren):
    # json_url = '''http://image.baidu.com/search/acjson?tn=resultjson_com&ie=utf-8&pn=%s&word=%s&rn=%s&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1#'''
    json_url = '''http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%s&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=ala&pn=%s&rn=%s&gsm=3c&1450340113203#'''
    key_word = []
    for item in word:
        a = urllib.quote(item)
        key_word.append(a)

    key_word_string = '+'.join(key_word)
    pre_name = '_'.join(word)

    url = json_url % (key_word_string, key_word_string, str(start), str(ren))
    print url

    headers = {'Accept': 'image/webp',
               'User-Agent': '''Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6''',}
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

    i = start
    for result in result_pic:
        real_url = parse_url(result)
        # real_url = result
        # print real_url
        i += 1
        pic_name = "%s_%s.jpg" % (pre_name, str(datetime.datetime.now().second) + '_' + str(i))

        print 'downloading pic No.%s' % str(i)

        if not os.path.exists('pics'):
            os.mkdir('pics')
        name = 'pics/%s' % pic_name
        if os.path.isfile(name):
            os.remove(name)
        try:
            socket.setdefaulttimeout(20)
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
            # f = open(name%str(i),'w+')
            # f.write(content)
            # f.close()


def my_crawler(s_num, e_num, word):
    i = s_num
    num = e_num - s_num
    while num / 60 != 0:
        baidu_crawler(i, word, 60)
        i += 60
        num -= 60

    baidu_crawler(i, word, num)


if __name__ == '__main__':

    args = sys.argv
    if len(args) < 4:
        print u'参数格式错误'
        print u'格式：python baidu_crawler.py start_num end_num word\nstart_num:开始序号\nend_num:结束序号\nword:关键字(关键字可以用空格隔开)'
        sys.exit(0)
    start_num = int(args[1])
    end_num = int(args[2])
    word = args[3:]

    my_crawler(start_num, end_num, word)
