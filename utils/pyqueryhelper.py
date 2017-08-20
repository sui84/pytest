#encoding=utf-8
from pyquery import PyQuery as pq
import reqhelper
import requests

class PyqueryHelper(object):
    def __init__(self):
        print 'fff'

     #先获取到so_md5key的值
    def SearchBD(self,keyword):
        print 'aaa'

def OnStart():
    d=pq(url='http://www.sobaidupan.com')
    so_md5key = d('[name="so_md5key"]').val()
    keyword = "pyspider"
    url="http://www.sobaidupan.com/search.asp?wd=%s&so_md5key=%s" % (keyword,so_md5key)
    d=pq(url=url)
    resultes=d('.search_box_list_bt a')
    cnt = d('.search_box_list_bt a').length
    urls = []
    for i in range(0,cnt):
        result = d('.search_box_list_bt a')
        href = result.eq(i).attr('href')
        name = result.eq(i).text()
        '''div = d('.search_box_list_bt')
        print div.next('p').eq(i).text()
        info = div.next('p').eq(i).text()
        print info.encode('gb2312','ignore')
        info += div.next('p').next('p').eq(i).text()'''
        print href,name
        urls.append({"name":name,"href":href})
        IndexPage(url)

def IndexPage(url):
    d=pq(url=url)
    bdurl=d('.pan_down > a').attr('href')
    d=pq(url=bdurl)
    print d


if __name__ == '__main__':
    #IndexPage("http://pdown.baidudaquan.com/down.asp?id=115228132&amp;token=2488fbae5d88060338a6955d3903eedf&amp;bt=pyspider-master.zip")
    headers={"Host":"pdown.baidudaquan.com"
             ,"Connection":"keep-alive"
            ,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            ,'Accept-Encoding':"gzip,deflate"
            ,'Accept-Language':"zh-CN,zh;q=0.8"
            ,'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 BIDUBrowser/6.x Safari/537.36"
            ,'Content-Type':"application/x-www-form-urlencoded"
            ,'Cookie': "ASPSESSIONIDQATQRTRQ=LDMGIGKAKJOHFOGHCAKLOBHB"}
    url1="http://www.sobaidupan.com/file-115228132.html"
    url2="http://pdown.baidudaquan.com/down.asp?id=107665964&token=06343750e8d2200e45563b8037e7e365&bt=Spider"
    #https://pan.baidu.com/share/link?shareid=3867566675&uk=3308350462#list/path=%2F
    #http://www.sobaidupan.com/file-107665964.html
    req = reqhelper.ReqHelper()
    #req.SaveHtmlAfterLogin(geturl=url)
    #https://www.douban.com/note/574012671/
    with requests.Session() as s:
        s = requests.Session()
        r = s.get(url1,headers=headers)
        r = s.get(url2,headers=headers)
        print r.text.encode('utf8')
        f = file(r"d:\temp\test.html", "w")
        f.write(r.text.encode('utf8'))
        f.close()



