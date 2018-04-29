#!usr/bin/python
# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq
from db import sqlhelper
import pymysql
import setting

mysqldb = setting.YAMLDATA.get('mysqldb2')
host,user,pwd,db=mysqldb.get('host'),mysqldb.get('user'),mysqldb.get('pwd'),mysqldb.get('cmfishdb')
host='127.0.0.1'
sh=sqlhelper.SqlHelper(host,user,pwd,db,'mysql')

class GetProxy(object):
    def __init__(self):
        # 代理ip网站
        self.url = 'http://www.xicidaili.com/nn/%d'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        # 用于检查代理ip是否可用
        #self.check_url = 'https://www.python.org/'
        self.check_url = 'http://ip.chinaz.com/getip.aspx'
        self.title = 'Welcome to Python.org'


    def get_page(self,page):
        response = requests.get(self.url % page, headers=self.header)
        # print(response.status_code)
        return response.text

    def page_parse(self, response):
        ips = []
        stores = []
        result = pq(response)('#ip_list')
        for p in result('tr').items():
            if p('tr > td').attr('class') == 'country':
                ip = p('td:eq(1)').text()
                port = p('td:eq(2)').text()
                protocol = p('td:eq(5)').text().lower()
                # if protocol == 'socks4/5':
                #     protocol = 'socks5'
                if port <> '80':
                    proxy = '{}://{}:{}'.format(protocol, ip, port)
                    stores.append(proxy)
                    ips.append(ip)
        return stores,ips

    def start(self,page=1):
        response = self.get_page(page)
        proxies,ips = self.page_parse(response)
        print(len(proxies))
        print ips
        i,j = 0,0
        for proxy in proxies:
            try:
                check_char = ""
                check = requests.get('http://www.cmfish.com/bbs/?1', headers=self.header, proxies={'http': proxy}, timeout=3)
                #print ips[i],check.text
                #if ips[i] in check.text:
                #check_char = pq(check.text)('head > title').text()
                #if check_char == self.title:
                print('%s is useful' % proxy)
                sql = "insert into proxy(proxy) values('%s')" % proxy
                sh.ExecNonQuery(sql)
                j += 1
                i += 1
            except Exception,e:
                continue
                '''
                import time
                import traceback
                print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()
               '''
        if j == 0:
            self.start(page+1)
        print('Get %s proxies'%j)

    def starts(self):
        for i in range(1,5):
            self.start(i)

if __name__ == '__main__':
    get = GetProxy()
    get.starts()
