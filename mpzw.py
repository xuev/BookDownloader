#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
-------------------------------------------------
@Author:        xuev
@Contact:       xuewei918@gmail.com
@Project:       BookDownloader
@FileName:      mpzw.py
@Version:       0.0.1
@License:       MIT Licence
@Created on:    2017/12/13 02:48
@Description:   Download book from http://www.mpzw.com
-------------------------------------------------
"""

import sys
import requests
from bs4 import BeautifulSoup
import threading
import time
import re
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
        params = {"q": self.b_name, "entry": 1, "s": 1462921654728649351}   # 搜索栏参数
        url = "http://zhannei.baidu.com/cse/search"
        try:
            r = requests.get(url, params=params)
            r.encoding = "utf-8"
            if r.url == "http://www.baidu.com/search/error.html":
                return False
            else:
                bs_obj = BeautifulSoup(r.text, "lxml").findAll("a", {"cpos": "title"})[1]   # 搜索结果的列表顺序
                print bs_obj["href"]
                return bs_obj["href"]
        except:
            print("获取目录失败,一秒后重试，失败链接：", url, params)
            time.sleep(3)
            self.b_link_load()

    def directory(self):
        link = self.b_link[:-10]
        links = []
        r = requests.get(self.b_link)
        r.encoding = "gbk"
        bs_obj = BeautifulSoup(r.text, "lxml").find_all("td", {"class": "ccss"})
        for i in bs_obj:
            try:
                url = link + i.a["href"]
                sec_name = re.sub("\n", "", i.get_text())
                links.append((url, sec_name))
            except:
                print(i, "获取章节链接错误")
        print links
        return links

    def section_load(self, links):
        for i in links:
            try:
                r = requests.get(i[0])
                r.encoding = "gbk"
                bs_obj = BeautifulSoup(r.text, "lxml").find(id="clickeye_content")
                if bs_obj != None:
                    content = bs_obj.get_text("\n", strip=True)
                    # content = re.compile("(猫扑中文 www.mpzw.com)    ").sub("", content)
                self.content[i[1]] = content
                print(i[1], "抓取完成")
            except (TypeError, AttributeError):
                print("*" * 10, "%s章节错漏" % i[1])
            except:
                print("*" * 20, "%s抓取错误，重试中" % i[1])
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
        for i in self.b_directory:
            try:
                title = "\n\n" + i[1] + "\n"
                f.write(title)
                f.write(self.content[i[1]])
            except KeyError:
                print("*" * 10, "缺失章节为：", i[1])
        f.close()

if __name__ == '__main__':
    book = load_book("最强雇佣兵")
    book.contents_load(10)
    book.write_txt()