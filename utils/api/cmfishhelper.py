#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import requests
from bs4 import BeautifulSoup
import pprint
from utils.db import sqlhelper
from utils import setting
import re
import pymysql
import traceback
from requests.utils import get_encoding_from_headers, get_encodings_from_content
import urllib2
import json

typeto,pageto = 7,5
cardurls = "http://www.cmfish.com/cd/cd_style.php?id=%d"
cdpages = "http://www.cmfish.com/cd/cd_style.php?pageNum_Recordset1=%d&totalRows_Recordset1=191&id=1"
mysqldb = setting.YAMLDATA.get('mysqldb2')
host,user,pwd,db=mysqldb.get('host'),mysqldb.get('user'),mysqldb.get('pwd'),mysqldb.get('cmfishdb')
sh=sqlhelper.SqlHelper(host,user,pwd,db,'mysql')
cardidrec=re.compile('((id=)([^&][^&]*))', re.IGNORECASE)
hotrec=re.compile('((hot=)([^&][^&]*))', re.IGNORECASE)
daterec=re.compile('(\xbc\xd3\xc8\xeb\xc8\xd5\xc6\xda: ([\\s\\S]*?)</td>)', re.IGNORECASE)
namerec=re.compile('(</a> &gt; <strong>([\\s\\S]*?)</strong>)', re.IGNORECASE)
contactrec=re.compile('(\xc1\xaa \xcf\xb5 \xc8\xcb</td>\r\n                              <td>([\\s\\S]*?)</td>)', re.IGNORECASE)
mobilerec=re.compile('(\xc1\xaa\xcf\xb5\xb5\xe7\xbb\xb0</td>\r\n                              <td>([\\s\\S]*?)</td>\r\n)', re.IGNORECASE)
mailrec=re.compile('(\xb5\xe7\xd7\xd3\xd3\xca\xcf\xe4</td>\r\n                              <td>([\\s\\S]*?)</td>\r\n)', re.IGNORECASE)
addressrec=re.compile('(\xc1\xaa\xcf\xb5\xb5\xd8\xd6\xb7</td>\r\n                              <td>([\\s\\S]*?)</td>\r\n)', re.IGNORECASE)
noterec=re.compile('(<td>&nbsp;&nbsp;&nbsp;&nbsp;([\\s\\S]*?)</td>\r\n)', re.IGNORECASE)

def get_cds():
    cds = []
    for i in range(1,typeto+1):
        for j in range(0,pageto):
            url = 'http://www.cmfish.com/cd/cd_style.php?pageNum_Recordset1=%d&totalRows_Recordset1=191&id=%d' % (j,i)
            req=requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            links=soup.find_all('a')
            for link in links:
                href = link.attrs['href']
                if "cd.php?id=" in href and href<>'cd.php?id=&hot=':
                    cdlink = "http://www.cmfish.com/cd/"+href
                    pprint.pprint(cdlink)
                    save_cd(i,j,cdlink)
                    cds.append(cdlink)
    return cds

def save_cd(typeid,pageid,url):
    sql = r"insert into card(typeid,pageid,url) values(%d,%d,'%s')" % (typeid,pageid,url)
    sh.ExecNonQuery(sql)

def re_result(strrec,str,value):
    searched = strrec.findall(str)
    if searched <> None and len(searched)>0:
        pprint.pprint(searched[0][1])
        try:
            return searched[0][1].decode('gb2312')
        except:
            return searched[0][1].decode('gbk')
    else:
        return value

def url_result(strrec,str,value):
    searched = strrec.findall(str)
    if searched <> None and len(searched)>0:
        print searched[0][2]
        return searched[0][2]
    else:
        return value

def get_detail(selsql,updsql):
    results=sh.ExecQuery(selsql)
    for result in results:
        try:
            id,url=result[0],result[1]
            cardid,hot = url_result(cardidrec,url,''),url_result(hotrec,url,0)
            #req = requests.get(url)
            #req.encoding=get_encodings_from_content(req.content)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            content = response.read()

            date = re_result(daterec,content,'')
            name = re_result(namerec,content,'')
            contact = re_result(contactrec,content,'')
            mobile=re_result(mobilerec,content,'')
            mail = re_result(mailrec,content,'')
            address = re_result(addressrec,content,'')
            note = re_result(noterec,content,'')
            sql = updsql % (cardid,hot,pymysql.escape_string(date),pymysql.escape_string(name),pymysql.escape_string(contact),pymysql.escape_string(mobile),pymysql.escape_string(mail),pymysql.escape_string(address),pymysql.escape_string(note),id)
            sh.ExecNonQuery(sql)
        except Exception,e:
            print 'error:',e.message,traceback.format_exc()

def update_cds():
    selsql= "select id,url from card where cardid is null"
    updsql = "update card set cardid=%s,hot=%s,date='%s',name='%s',contact='%s',mobile='%s',mail='%s',address='%s',note='%s' where id=%d"
    get_detail(selsql,updsql)

def get_lnglat(address):
     print address
     url = 'http://api.map.baidu.com/geocoder/v2/'
     output = 'json'
     ak = 'c7aBgFWD6cMDPOe4BSiG8HLNlvXNKvCW'
     uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
     temp = urllib2.urlopen(uri)
     temp = json.loads(temp.read())
     return temp

def save_lnglat(selsql,updsql):
    results=sh.ExecQuery(selsql)
    for result in results:
        try:
            id,address=result[0],result[1]
            if '例如' not in address:
                address = address.replace(' ',',')
                result = get_lnglat(address)
                if result.get('result') <> None:
                    lat,lng = result.get('result').get('location').get('lat'),result.get('result').get('location').get('lng')
                    sql = updsql % (lat,lng,id)
                    sh.ExecNonQuery(sql)
        except Exception,e:
            print 'error:',e.message,traceback.format_exc()
            #result[1]

def update_lnglat():
    selsql= "select id,address from card where lat is null"
    updsql = "update card set lat=%f,lng=%f where id=%d"
    save_lnglat(selsql,updsql)

def gen_json(ofile='./../json/cards.json'):
    selsql = "select name,lat,lng from card where lat is not null"
    results=sh.ExecQuery(selsql)
    objs = []
    #objs.append({"name":results[0][0],"lat":float(results[0][1]),"lng":float(results[0][2])})
    #objs.append({"name":results[1][0],"lat":float(results[1][1]),"lng":float(results[1][2])})
    for res in results:
        objs.append({"name":res[0],"lat":float(res[1]),"lng":float(res[2])})
    jsonstr =json.dumps(objs)
    with open(ofile,'w') as f:
            f.write(jsonstr)
    print jsonstr

if __name__ == '__main__':
    #cds = get_cds()
    #print len(cds)
    #update_cds()
    #print get_lnglat('台灣省桃園縣龜山鄉振興路1089巷15-1號')
    #update_lnglat()
    gen_json()
