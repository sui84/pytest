#encoding=utf-8
from pyquery import PyQuery as pq
import reqhelper
import requests
import timehelper
import confhelper
import sys
sys.path.append("DB")
import sqlhelper

class PyqueryHelper(object):
    def __init__(self):
        print 'fff'

     #region 先获取到so_md5key的值，失败了

def BaiduWangPan():
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
    #endregion

def SaveToDB(ymon,day,seq,name,title,url):
    conf = confhelper.ConfHelper()
    dbinfo = conf.GetSectionConfig("mysqldb")
    mydb = sqlhelper.SqlHelper(host=dbinfo.get("mysqlhost"), user=dbinfo.get("mysqluser"), pwd=dbinfo.get("mysqlpwd"), db=dbinfo.get("mysqldb"),dbtype='mysql')
    sqlstr = "insert into huodong(year,month,day,seq,name,title,url) select %d,%d,%d,%d,'%s','%s','%s' from DUAL where not exists (select 1 from huodong where  year=%d and month=%d and day = %d and url='%s')" \
             % (ymon.get("year"),ymon.get("month"),day,seq,name,title,url,ymon.get("year"),ymon.get("month"),day,url)
    print sqlstr
    mydb.ExecNonQuery(sqlstr)
    sqlstr = "update huodong set name='%s',title='%s' where year=%d and month=%d and day = %d and url='%s'" \
             % (name,title,ymon.get("year"),ymon.get("month"),day,url)
    print sqlstr
    mydb.ExecNonQuery(sqlstr)


def ZhuhaiHuWai(ymon):
    huodong = confhelper.ConfHelper().GetConfig("zhhuwai","huodong")
    t = timehelper.TimeHelper()
    url = huodong % ("%d%02d" % (ymon.get("year"),ymon.get("month")))
    print url
    d=pq(url=url)
    td = d("#z_tb_ecal tr td")
    #div = d("#z_tb_ecal tr td div")
    cnt = td.length

    for i in range(0,cnt):
        day = td.eq(i).find('div').text()
        tda =  td.eq(i).find('p a')
        tdacnt = tda.length
        for j in range(0,tdacnt):
            name = tda.eq(j).text()
            href = tda.eq(j).attr.href
            title = tda.eq(j).attr.title
            SaveToDB(ymon,int(day),j,name,title,href)

    #resList = mydb.ExecQuery("SELECT * FROM urls")
    #print resList

def GetZhuhaiHuWai():
    #获取当前月份开始的1年
    t = timehelper.TimeHelper()
    ymons = t.GetYearMonths(12)
    for ymon in ymons:
        #curmonth=timehelper.TimeHelper().GetCurrentTimeStr(fmt='%Y%m')
        ZhuhaiHuWai(ymon)

if __name__ == '__main__':
    GetZhuhaiHuWai()


