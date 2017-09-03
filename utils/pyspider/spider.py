#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-03-29 10:59:36
# Project: taonvlang
import os
from pyspider.libs.base_handler import *
import pyspider.database.mysql.sqlhelper as sqlhelper

DIR_PATH = '/usr/project/taobaomm'

class Handler(BaseHandler):
    crawl_config = { }

    def __init__(self):
        self.base_url = "https://mm.taobao.com/json/request_top_list.htm?page"
        self.page_num = 1
        self.total_num = 30

    @every(minutes=24 * 60)
    def on_start(self):
        while self.page_num <= self.total_num:
            url = self.base_url + str(self.page_num)
            print url
            self.crawl(url, callback=self.index_page)
            self.page_num += 1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc("a[href^='http']").items():
             self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        #return { "url": response.url, "title": response.doc('title').text(),
        print "detail_page"
        name = response.doc('.mm-p-model-info-left-top dd > a').text()
        dir_path = self.mkDir(name)
        #先抓大再抓小
        brief = response.doc('.mm-aixiu-content').text()
        imgs = response.doc('.mm-aixiu-content img').items()
        count = 1
        self.saveBrief(brief, dir_path, name)
        for img in imgs:
            url = img.attr.src
            if url:
                print url
                count += 1
                extension = self.getExtension(url)
                file_name = name + str(count) + '.' + extension
                self.crawl(img.attr.src, callback=self.save_img, save={'dir_path': dir_path, 'file_name': file_name}, validate_cert=False)

                return {
                "name":name,
                "url": response.url,
                "title": response.doc('title').text(),
                        }

    def on_result(self, result):
        #print result
        if not result or not result['name']:
            return
        ms = sqlhelper.SqlHelper()
        sqlstr = "insert into urls(name,url) values(%s,%s)" % (result['name'],result['name'])
        resList = ms.ExecQuery(sqlstr)


    #抓到图片后保存
    def save_img(self, response):
        content = response.content
        dir_path = response.save['dir_path']
        file_name = response.save['file_name']
        file_path = dir_path + '/' + file_name
        self.saveImg(content, file_path)

    def mkDir(self, path):
        path = path.strip()
        dir_path = DIR_PATH + path
        exists = os.path.exists(dir_path)
        if not exists:
            os.makedirs(dir_path)
            return dir_path
        else:
            return dir_path

    def saveImg(self, content, path):
        f = open(path, 'wb')
        f.write(content)
        f.close()

    def saveBrief(self, content, dir_path, name):
        file_name = dir_path + "/" + name + ".txt"
        f = open(file_name, "w+")
        f.write(content.encode('utf-8'))

    def getExtension(self, url):
        extension = url.split('.')[-1]
        return extension

