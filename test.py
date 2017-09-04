#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  xuev (xuewei918@gmail.com)
@Project: BookDownloader
@File: test.py
@Version: 0.01
@License: MIT Licence
@Create Time: 2017/8/12 21:27
@Description: 
"""

import requests
from bs4 import BeautifulSoup


def directory(name):
    # headers = {
    #     'Host': "zhannei.baidu.com",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding": "gzip, deflate",
    #     'Accept-Language': "zh-CN,zh;q=0.8,en;q=0.6",
    #     "Connection": "keep-alive",
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
    # }
    params = {"q": name, "entry": 1, "s": 1101330821780029220, "isNeedCheckDomain": 1, "jump": 1}
    url = "http://zhannei.baidu.com/cse/search"
    print(url)
    # r = requests.get(url, headers=headers, params=params)
    r = requests.get(url, params=params)
    r.encoding = "utf-8"
    if r.url == "http://www.baidu.com/search/error.html":
        return False
    else:
        bsObj = BeautifulSoup(r.text, "lxml").findAll("a", {"cpos": "title"})[0]
        print bsObj["href"], bsObj.get_text()[1:-1]
        return bsObj["href"], bsObj.get_text()[1:-1]


def contents(url):
    link = url[:-10]
    print(link)
    links = []
    r = requests.get(url)
    r.encoding = 'gbk'
    bsObj = BeautifulSoup(r.text, "lxml").findAll("dd")
    for i in bsObj:
        url = link + i.a["href"]
        links.append((url, i.get_text()))
    print links


def section(url):
    r = requests.get(url)
    r.encoding = "gbk"
    bsObj = BeautifulSoup(r.text, "lxml").find(id="BookText").findAll("p")

    print bsObj

# directory("最强神眼")
section("http://www.vodtw.com/html/book/19/19074/10220380.html")
