#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  xuev (xuewei918@gmail.com)
@Project: BookDownloader
@File: BookDownloader.py
@Version: 0.01
@License: MIT Licence
@Create Time: 2017/8/12 19:16
@Description: 
"""

import requests
from bs4 import BeautifulSoup
import re
import threading
import time
from io import open
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class load_book(object):
    def __init__(self, book_name):
        self.b_name = book_name
        self.b_link = self.b_link_load()
        self.b_directory = self.directory()
        self.content = {}

    def b_link_load(self):
        params = {"q": self.b_name, "entry": 1, "s": 1462921654728649351, "isNeedCheckDomain": 1, "jump": 1}
        url = "http://zhannei.baidu.com/cse/search"
        try:
            r = requests.get(url, params=params)
            r.encoding = "utf-8"
            if r.url == "http://www.baidu.com/search/error.html":
                return False
            else:
                # bsObj = BeautifulSoup(r.text, "lxml").findAll("a", {"cpos": "title"})[1]
                # return bsObj["href"]
                aaa = 'http://www.mpzw.com/html/142/142270/index.html'
                return aaa
        except:
            print("获取目录失败,一秒后重试，失败链接：", url, params)
            time.sleep(1)
            self.b_link_load()

    def directory(self):
        link = self.b_link[:-10]
        links = []
        r = requests.get(self.b_link)
        r.encoding = "gbk"
        links = [('http://www.mpzw.com/html/142/142270/30966207.html', u'第二章 离异美女')]
        # bbb = r.text
        # bsObj = BeautifulSoup(r.text, "lxml").findAll("a")
        # for i in bsObj:
        #     try:
        #         url = link + i["href"]
        #         # ccc = url
        #         links.append((url, i.get_text()))
        #     except TypeError:
        #         print(i, "获取章节链接错误")
        print links
        return links

    def section_load(self, links):
        for i in links:
            try:
                r = requests.get(i[0])
                r.encoding = 'gbk'
                bsObj = BeautifulSoup(r.text, "lxml").find(id="cont")
                content = [content.text for content in bsObj.find_all('div', {'id': 'clickeye_content'})]
                # content = '\n'.join(content)

                # content = re.compile(r"<!--章节内容开始-->(.*)<!--章节内容结束-->").search(str(bsObj))  # 把章节内容提取出来
                # content = re.compile("<br/><br/>").sub("\n", content.group(1))  # 把网页的<br/><br/>替换成换行符
                # self.content[i[1]] = content[:-8]
                # ccc = content[i]
                # self.content[i[1]] = 'aaabbbccc'
                print(i[1], "抓取完成")
            except (TypeError, AttributeError):
                print("*" * 10, "%s章节错漏" % i[1])
            except:
                print("*" * 10, "%s抓取错误，重试中" % i[1])
                links.insert(0, i)

    def contents_load(self, loops=10):
        threads = []
        nloops = range(loops)
        task_list = []
        task_size = len(self.b_directory) // loops + 1
        for i in nloops:  # 分割任务
            try:
                task_list.append(self.b_directory[i * task_size:(i + 1) * task_size])
            except:
                task_list.append(self.b_directory[i * task_size:])

        for i in nloops:
            t = threading.Thread(target=self.section_load, args=([task_list[i]]))
            threads.append(t)

        for i in nloops:
            threads[i].start()

        for i in nloops:
            threads[i].join()

    def write_txt(self):
        print("开始制作txt文档")
        f = open(self.b_name + ".txt", "w", encoding="utf-8")
        # f.write(" " * 20 + self.b_name + "\n")
        ddd = self.b_directory
        for i in self.b_directory:
            try:
                title = "\n\n" + " " * 20 + i[1] + "\n"
                f.write(title)
                ddd = self.content[i]
                f.write(self.content[i[1]])
            except KeyError:
                print("*" * 10, "缺失章节为：", i[1])
        f.close()


if __name__ == '__main__':
    book = load_book("猛男诞生记")
    book.contents_load(10)
    book.write_txt()
