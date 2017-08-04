#encoding=utf-8
import time
import traceback
import requests
import json
import confhelper


class ReqHelper(object):
    def __init__(self, url=r'http://www.baidu.com',headers={}, outfile=r'd:\temp\test.html',proxies={},timeout=3):
        self.conf=confhelper.ConfHelper(r'd:\temp\test.conf')
        self.confs=self.conf.GetAllConfig()
        if not(url.startswith('http://')) and not(url.startswith('https://')):
            url = 'http://'+url
        if len(proxies)==0 and self.confs.has_key("username") and self.confs.has_key("password") and self.confs.has_key("httpserver"):
            proxies['http'] ="http://%s:%s@%s"%(self.confs["username"],self.confs["password"],self.confs["httpserver"])
            proxies['https'] ="http://%s:%s@%s"%(self.confs["username"],self.confs["password"],self.confs["httpsserver"])
        self.proxies = proxies
        if len(headers)=0:
            headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                                            ,'Accept-Encoding':'gzip,deflate,sdch'
                                            ,'Accept-Language':'zh-CN,zh;q=0.8'
                                            ,'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
                                            ,'Content-Type':'application/x-www-form-urlencoded'}
        self.headers = headers
        self.url = url
        if outfile="" and self.confs.has_key("logpath"):
            outfile=self.confs["logpath"]
        self.outfile = outfile
        self.session = requests.session()
        self.session.proxies=self.proxies
        
        
    def TestUrls(self):
        httpurls=self.conf.GetSectionConfig("httpurl")
        httpsurls=self.conf.GetSectionConfig("httpsurl")
        urls=dict(httpurls,**httpsurls)
        for (urlkey,url) in urls.items():
            try:
                print time.ctime(),"Start testing url : %s"%(url)
                r = requests.get(url, proxies=self.proxies,timeout=3)
                print time.ctime(),"Reponse status code :",r.status_code
                SaveHtmlContent(r,self.outfile,'a')
            except Exception,e:
                print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()

    def SaveHtml(self, user='', password = '', outfile=''):
        r = requests.get(self.url, auth=(user, password))
        SaveHtmlContent(r,outfile,'w')

    def SaveHtmlAfterLogin(self, geturl, user='', password = '',outfile=''):
        r = requests.get(self.url, auth=(user, password))
        s = requests.Session()
        r = s.get(geturl)
        SaveHtmlContent(r,outfile,'w')

    def SavePostResponse(self, data={}, cookies={} , outfile=''):
        r = requests.post(self.url,data=data, cookies=cookies)
        SaveHtmlContent(r,outfile,'w')

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
    def SaveHtmlContent(r,outfile="",writemode='a'):
        if outfile="" and writemode='a' and self.confs.has_key("logpath"):
            outfile = self.confs["logpath"]
        if outfile="" and writemode='w' and self.confs.has_key("htmlpath"):
            outfile = self.confs["htmlpath"]
        f = file(outfile, writemode)
        content = 
        if writemode='a':
        f.write(r.text.encode('utf8'))
        f.close()


if __name__ == '__main__':
    print 'ReqHelper'

