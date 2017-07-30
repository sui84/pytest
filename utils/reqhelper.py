#encoding=utf-8
import requests
import json


class ConfHelper(object):
    def __init__(self, url=r'http://www.baidu.com', outfile=r'd:\temp\test.html'):
        if not(url.startswith('http://')) and not(url.startswith('https://')):
            url = 'http://'+url
        self.url = url
        self.outfile = outfile

    def SaveHtml(self, user='', password = '', outfile=''):
        r = requests.get(self.url, auth=(user, password))
        if outfile=='':
            f = file(self.outfile, 'w')
        else:
            f = file(outfile, 'w')
        f.write(r.text.encode('utf8'))
        f.close()

    def SaveHtmlAfterLogin(self, geturl, user='', password = '',outfile=''):
        r = requests.get(self.url, auth=(user, password))
        s = requests.Session()
        r = s.get(geturl)
        if outfile=='':
            f = file(self.outfile, 'w')
        else:
            f = file(outfile, 'w')
        f.write(r.text.encode('utf8'))
        f.close()

    def SavePostResponse(self, data={}, cookies={} , outfile=''):
        r = requests.post(self.url,data=data, cookies=cookies)
        if outfile == '':
            f = file(self.outfile, 'w')
        else:
            f = file(outfile, 'w')
        f.write(r.text.encode('utf8'))
        f.close()

    def SaveResponseWithCookie(self, headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                                            ,'Accept-Encoding':'gzip,deflate,sdch'
                                            ,'Accept-Language':'zh-CN,zh;q=0.8'
                                            ,'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
                                            ,'Content-Type':'application/x-www-form-urlencoded'}
                    , cookies={}):
        r = requests.get(self.url, headers=headers,cookies=cookies);
        f = file(self.outfile, 'w')
        f.write(json.dumps(r.headers.__dict__))
        f.write('\n')
        f.write(r.text.encode('utf8'))
        f.close()
    def GetCookies(self, user='', password = ''):
        r = requests.get(self.url, auth=(user, password))
        return r.headers["Set-Cookie"]


