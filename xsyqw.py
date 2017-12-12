#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
-------------------------------------------------
@Author:        xuev
@Contact:       xuewei918@gmail.com
@Project:       BookDownloader
@FileName:      xsyqw.py
@Version:       0.0.1
@License:       MIT Licence
@Created on:    2017/12/9 03:55
@Description:   ...
-------------------------------------------------
"""

import sys
import requests
import re
import threading
from bs4 import BeautifulSoup
import time
from io import open

reload(sys)
sys.setdefaultencoding('utf-8')


class load_book(object):
    def __init__(self, book_name):
        self.b_name = book_name
        self.b_link = self.b_link_load()
        self.b_directory = self.directory()
        self.content = {}

    def b_link_load(self):
        try:
            book_link = 'http://www.xsyqw.com/files/article/html/8/8640/index.html'
            return book_link
        except:
            # print("获取目录失败,一秒后重试，失败链接：", url, params)
            return False

    def directory(self):
        link = self.b_link[:-10]
        print link
        links = []
        r = requests.get(self.b_link)
        r.encoding = "gb2312"
        bsObj = BeautifulSoup(r.text, "lxml").findAll("li")
        print '获取章节链接...'
        for i in bsObj:
            try:
                url = link + i.a["href"]
                # print url
                # print i.get_text()
                links.append((url, i.get_text()))
            except TypeError:
                print(i, "获取章节链接错误")
        print '章节链接获取完成.'
        return links

    def section_load(self, links):
        print '获取章节内容...'
        for i in links:
            try:
                r = requests.get(i[0])
                r.encoding = "gb2312"
                bs_obj = BeautifulSoup(r.text, "lxml").find(id="htmlContent")
                if bs_obj != None:
                    content = bs_obj.get_text("\n", strip=True)
                self.content[i[1]] = content
                print (i[1], u"抓取完成")

            except (TypeError, AttributeError):
                print ("*" * 10, "%s 章节错漏" % i[1])
            except:
                print ("*" * 10, "%s 抓取错误，重试中" % i[1])
            # links.insert(0, i)
        print '章节内容获取完成.'

    def contents_load(self, loops=1):
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
        print ("开始制作txt文档")
        f = open(self.b_name + ".txt", "w", encoding="utf-8")
        for i in self.b_directory:
            try:
                title = "\n\n" + i[1] + "\n"
                f.write(title)
                if self.content[i[1]] != None:
                    f.write(self.content[i[1]])
            except KeyError:
                print ("*" * 10, "缺失章节为：", i[1])
        f.close()


if __name__ == '__main__':
    book = load_book("桃针医少")
    book.contents_load(10)
    # book.section_load(links=book.b_directory)
    book.write_txt()
