#encoding=utf-8
import time
import traceback
import requests
import json
import confhelper
import os
from bs4 import BeautifulSoup #__version__ = 4.3.2
from urlparse import urljoin
import threadpool


class ReqHelper(object):
    def __init__(self, url=r'http://www.baidu.com',headers={}, outfile=r'd:\temp\log.txt',proxies={},timeout=3):
        path=r'd:\temp\test.conf'
        if os.path.exists(path):
            self.conf=confhelper.ConfHelper(path)
            self.confs = self.conf.GetAllConfig()
        if not(url.startswith('http://')) and not(url.startswith('https://')):
            url = 'http://'+url
        #代理格式 http://user:password@host/
        if len(proxies)==0 and self.confs.has_key("username") and self.confs.has_key("password") and self.confs.has_key("httpserver"):
            proxies['http'] ="http://%s:%s@%s"%(self.confs["username"],self.confs["password"],self.confs["httpserver"])
            proxies['https'] ="http://%s:%s@%s"%(self.confs["username"],self.confs["password"],self.confs["httpsserver"])
        self.proxies = proxies
        #SOCKS 代理格式 socks5://user:pass@host:port
        '''proxies = {
            'http': 'socks5://user:pass@host:port',
            'https': 'socks5://user:pass@host:port'
        }'''
        if len(headers)==0:
            headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                                            ,'Accept-Encoding':'gzip,deflate,sdch'
                                            ,'Accept-Language':'zh-CN,zh;q=0.8'
                                            ,'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
                                            ,'Content-Type':'application/x-www-form-urlencoded'}
        self.headers = headers
        self.url = url
        if outfile=="" and self.confs.has_key("logpath"):
            outfile=self.confs["logpath"]
        self.outfile = outfile
        self.session = requests.session()
        self.session.proxies=self.proxies
        if self.confs.has_key("theadnum") and self.confs["theadnum"].isdigit():
            self.theadnum = int(self.confs["theadnum"])
        else :
            self.theadnum = 10

    #下载文件到本地
    def DownloadFile(self,sourceurl,destdir):
        try:
            with requests.Session() as s:
                s = requests.Session()
                r = s.get(sourceurl,headers=self.headers)
                destfile = os.path.join(destdir,os.path.basename(sourceurl))
                with open(destfile,"wb") as file:
                    file.write(r.content)
                print time.ctime(), 'Download :',sourceurl,'\nTo :',destfile
        except Exception,e:
            print time.ctime(), 'Error :',e.message,'\n',traceback.format_exc()

    # 如果目录不存在就新建
    def GetDownloadPath(self,dp=""):
        if dp=="":
            dp=self.confs["downloadpath"]
        if not os.path.exists(dp):
            os.mkdir(dp)
        return dp

    # 按条件取出网页上所有href地址
    def GetHrefs(self,func, url):
        r = requests.get(url, proxies=self.proxies,headers=self.headers,timeout=3)
        bs = BeautifulSoup(r.text) #解析获取的网页
        links=bs.find_all('a')
        newls=filter(func,links)
        durls=[]
        for link in newls:
            hrefstr = link['href']
            if not hrefstr.startswith('http'):
                if not url.endswith('/'):
                    url = url + '/'
                durls.append(urljoin(url,hrefstr))
        #去重
        durls = list(set(durls))
        return durls

    # 下载网页上所有文件
    def DownloadUrlFiles(self,func=None,url="",dp=""):
        #func=lambda x:x['href'].endswith('.ipk')
        #func=None
        dp = self.GetDownloadPath(dp)

        data=[]
        if len(url) > 0:
            durls=self.GetHrefs(func,url)
            for durl in durls:
                data.append(((durl,dp), None))
        else:
            urls = self.conf.GetSectionConfig("downloadurlfiles")
            for (dkey,durl) in urls.items():
                destdir = os.path.join(dp,dkey)
                destdir = self.GetDownloadPath(destdir)
                durls = self.GetHrefs(func,durl)
                for durl in durls:
                    data.append(((durl,destdir), None))
        #for durl in durls:
        #    self.DownloadFile(durl,dp)
        #用多线程下载
        pool = threadpool.ThreadPool(self.theadnum)
        reqs = threadpool.makeRequests(self.DownloadFile, data)
        [pool.putRequest(req) for req in reqs]
        pool.wait()

    # 下载单个文件链接
    def DownloadUrlFile(self,url="",dp=""):
        dp = self.GetDownloadPath(dp)
        if len(url) > 0:
            self.DownloadFile(url,dp)
        else:
            urls = self.conf.GetSectionConfig("downloadurlfile")
            for (dkey,durl) in urls.items():
                #dfname = os.path.join(dp,fkey)
                self.DownloadFile(durl,dp)

    # 保存网页内容
    def SaveHtmlContent(self,r,outfile="",writemode='a'):
        if outfile == "" and writemode == 'a' and self.confs.has_key("logpath"):
            outfile = self.confs["logpath"]
        if outfile == "" and writemode == 'w' and self.confs.has_key("htmlpath"):
            outfile = self.confs["htmlpath"]
        f = file(outfile, writemode)
        if writemode=='a':
            lines=[r.request.method,'\n',r.request.url,'\n',str(r.headers),'\n',r.request.body,'\n',r.url,'\n',str(r.status_code),'\n', str(r.headers),'\n',r.text.encode('utf-8','ignore')]
            f.writelines(lines)
        if writemode=='w':
            f.write(r.text.encode('utf8'))
        f.close()

    # 测试网址是否能打开
    def TestUrls(self):
        httpurls=self.conf.GetSectionConfig("httpurl")
        httpsurls=self.conf.GetSectionConfig("httpsurl")
        urls=dict(httpurls,**httpsurls)
        for (urlkey,url) in urls.items():
            try:
                if not(url.startswith('http://')) and not(url.startswith('https://')):
                    url = 'http://'+url
                r = requests.get(url, proxies=self.proxies,headers=self.headers,timeout=3)
                print time.ctime(),r.url," Reponse status code :",r.status_code
                self.SaveHtmlContent(r,self.outfile,'a')
            except Exception,e:
                print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()

    def SaveHtml(self, user='', password = '', outfile=''):
        r = requests.get(self.url, auth=(user, password))
        self.SaveHtmlContent(r,outfile,'w')

    # 用同一个会话打开链接
    def SaveHtmlAfterLogin(self, geturl, user='', password = '',outfile=''):
        r = requests.get(self.url, auth=(user, password))
        s = requests.Session()
        r = s.get(geturl)
        self.SaveHtmlContent(r,outfile,'w')

    def SavePostResponse(self, data={}, cookies={} , outfile=''):
        r = requests.post(self.url,data=data, cookies=cookies)
        self.SaveHtmlContent(r,outfile,'w')

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



if __name__ == '__main__':
    print 'ReqHelper'

