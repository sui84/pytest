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
from pyquery import PyQuery as pq
import time
'''
http://echarts.baidu.com/examples/editor.html?c=effectScatter-bmap
https://github.com/airingursb/bilibili-user
'''

typeto,pageto = 7,5
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
proxy='http://123.53.118.58:61234'
cardurls = "http://www.cmfish.com/cd/cd_style.php?id=%d"
cdpages = "http://www.cmfish.com/cd/cd_style.php?pageNum_Recordset1=%d&totalRows_Recordset1=191&id=1"
usrurl = "http://www.cmfish.com/bbs/?%d"
ufriurl = "http://www.cmfish.com/bbs/home.php?mod=space&uid=%d&do=friend&from=space&page=%d"
mysqldb = setting.YAMLDATA.get('mysqldb2')
host,user,pwd,db=mysqldb.get('host'),mysqldb.get('user'),mysqldb.get('pwd'),mysqldb.get('cmfishdb')
host='127.0.0.1'
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
    selsql = "select name,lat,lng,typeid from card where lat is not null"
    results=sh.ExecQuery(selsql)
    objs = []
    for res in results:
        objs.append({"name":res[0],"lat":float(res[1]),"lng":float(res[2]),"typeid":int(res[3])})
    jsonstr =json.dumps(objs)
    with open(ofile,'w') as f:
            f.write(jsonstr)
    print jsonstr

def gen_gexf(ofile='./../gexf/test2.gexf'):
    import sys,pprint
    from gexf import Gexf


    # test helloworld.gexf
    gexf = Gexf("Gephi.org","A Web network")
    graph=gexf.addGraph("directed","static","A Web network")

    atr2 = graph.addNodeAttribute('modularity_class', 'Modularity Class', 'integer')

    tmp = graph.addNode("0","A")
    tmp.addAttribute(atr2,"0")

    tmp = graph.addNode("1","B")
    tmp.addAttribute(atr2,"0")


    graph.addEdge("0","0","1",weight='1')



    output_file=open(ofile,"w")
    gexf.write(output_file)

def save_user(uid,uname,url,verify,sex,birthdate,school,education,company,selfurl,fricnt,replycnt,pubcnt,point,prestige,gold ,ugroup,sign,livehours,regtime,lastviewtime,lastactiontime,lastpubtime,timezone):
    updsql="insert into users(uid,uname,url,verify,sex,birthdate,school,education,company,selfurl,fricnt,replycnt,pubcnt,point,prestige,gold ,ugroup,sign,livehours,regtime,lastviewtime,lastactiontime,lastpubtime,timezone) " \
           "values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,%d,%d,%d ,'%s','%s','%s','%s','%s','%s','%s','%s')"
    sql = updsql % (uid,pymysql.escape_string(uname),pymysql.escape_string(url),pymysql.escape_string(verify),pymysql.escape_string(sex),birthdate,pymysql.escape_string(school)
                    ,pymysql.escape_string(education),pymysql.escape_string(company),pymysql.escape_string(selfurl),fricnt,replycnt,pubcnt,point,prestige,gold ,pymysql.escape_string(ugroup),pymysql.escape_string(sign)
                    ,pymysql.escape_string(livehours),pymysql.escape_string(regtime),pymysql.escape_string(lastviewtime),pymysql.escape_string(lastactiontime),pymysql.escape_string(lastpubtime),pymysql.escape_string(timezone))
    sh.ExecNonQuery(sql)

def get_users(start,end):
    for uid in range(start,end):
        try:
            get_user(uid)
        except Exception,e:
            print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()

def get_user(uid):
    url=usrurl % uid
    #req = requests.get(url, headers=header, proxies={'http': proxy}, timeout=3)
    #d = pq(req.text)
    d = pq(url=url)
    parts=d('div.pbm.mbm.bbda.cl')
    uname = parts[0].find('h2').text.strip()
    #verify = remove_html(parts.eq(0).find('.pf_l').html())
    sign = parts.eq(0).find('table').text()
    infoarr=parts.eq(0).find('.pf_l.cl li').text().split()
    cntarr=d('.cl.bbda.pbm.mbm>li a')
    timearr=d('#pbbs li')
    pointarr = d('#psts li')
    verify,sex,birthdate,school,education,company,selfurl = split_infos(infoarr)
    fricnt,replycnt,pubcnt = split_cnts(cntarr)
    livehours,regtime,lastviewtime,lastactiontime,lastpubtime,timezone= split_times(timearr)
    point,prestige,gold = split_points(pointarr)
    ugroup = ""
    for li in d('.pbm.mbm.bbda.cl .xg1').items():
        ugroup+=li.text()+" "
    print "uid:%s,uname:%s,url:%s,verify:%s,sex:%s,birthdate:%s,school:%s,education:%s,company:%s,selfurl:%s,fricnt:%d,replycnt:%d,pubcnt:%d,point:%d,prestige:%d,gold:%d ,ugroup:%s,sign:%s" \
          ",livehours:%s,regtime:%s,lastviewtime:%s,lastactiontime:%s,lastpubtime:%s,timezone:%s" \
          % (uid,uname,url,verify,sex,birthdate,school,education,company,selfurl,fricnt,replycnt,pubcnt,point,prestige,gold ,ugroup,sign,livehours,regtime,lastviewtime,lastactiontime,lastpubtime,timezone)
    save_user(uid,uname,url,verify,sex,birthdate,school,education,company,selfurl,fricnt,replycnt,pubcnt,point,prestige,gold ,ugroup,sign,livehours,regtime,lastviewtime,lastactiontime,lastpubtime,timezone)
    #return uid,uname,url,verify,sex,birthdate,school,education,company,selfurl,fricnt,replycnt,pubcnt,point,prestige,gold ,ugroup,sign

    '''
    邮箱状态 已验证 视频认证 未认证 性别 保密 生日 - 毕业学校 计算机 学历 博士 公司 海友网 个人主页 http://
    好友数 58 记录数 0 日志数 0 相册数 0 回帖数 5372 主题数 695 分享数 0
    在线时间 18487 小时 注册时间 2005-6-20 13:06 最后访问 2018-4-15 12:31 上次活动时间 2018-4-15 08:53 上次发表时间 2018-4-14 17:30 所在时区 使用系统默认

    #re=u'(在线时间([\\s\\S]*?)注册时间([\\s\\S]*?)最后访问([\\s\\S]*?)上次活动时间([\\s\\S]*?)上次发表时间([\\s\\S]*?)所在时区([\\s\\S]*?))'
    re.split(u'好友数 |记录数 |日志数 |相册数 |回帖数 |主题数 |分享数 ',cntstr2)
    infore='((?!邮箱状态)([\\s\\S]*?)(?!视频认证)([\\s\\S]*?)(?!性别)([\\s\\S]*?)(?!生日)([\\s\\S]*?)(?!毕业学校)([\\s\\S]*?)(?!学历)([\\s\\S]*?)(?!公司)([\\s\\S]*?)(?!个人主页)([\\s\\S]*?))'
    cntre=u'((?!好友数)([\\s\\S]*?)(?!记录数)([\\s\\S]*?)(?!日志数)([\\s\\S]*?)(?!相册数)([\\s\\S]*?)(?!回帖数)([\\s\\S]*?)(?!主题数)([\\s\\S]*?)(?!分享数)([\\s\\S]*?))'
    timere=u'((?!在线时间)([\\s\\S]*?)(?!注册时间)([\\s\\S]*?)(?!最后访问)([\\s\\S]*?)(?!上次活动时)([\\s\\S]*?)(?!上次发表时间)([\\s\\S]*?)(?!所在时区)([\\s\\S]*?))'
    inforec=re.compile(infore,re.IGNORECASE)
    cntrec=re.compile(cntre,re.IGNORECASE)
    timerec=re.compile(timere,re.IGNORECASE)

    infores=inforec.findall(infostr)
    cntres=inforec.findall(cntstr)
    timeres=inforec.findall(timestr)
    '''

def split_infos(infos):
    verify,sex,birthdate,school,education,company,selfurl = "","","","","","",""
    for i in range(0,len(infos),2):
        if infos[i]=='邮箱状态' or infos[i]=='视频认证':
            verify += infos[i] + infos[i+1]+" "
        if infos[i]=='性别':
            sex += infos[i+1]
        if infos[i]=='生日':
            sex += infos[i+1]
        if infos[i]=='毕业学校':
            school += infos[i+1]
        if infos[i]=='学历':
            education += infos[i+1]
        if infos[i]=='公司':
            company += infos[i+1]
        if infos[i]=='个人主页':
            selfurl += infos[i+1]
    return verify,sex,birthdate,school,education,company,selfurl

def get_cnt(str):
    value=0
    num=re.findall(r"\d+",str)
    if len(num)>0:
        value = int(num[0])
    return value

def split_cnts(cntarr):
    fricnt,replycnt,pubcnt = 0,0,0
    for item in cntarr.items():
        if '好友数' in item.text():
            fricnt = get_cnt(item.text())
        if '回帖数' in item.text():
            replycnt = get_cnt(item.text())
        if '主题数' in item.text():
            pubcnt = get_cnt(item.text())
    return fricnt,replycnt,pubcnt

def split_times(liarr):
    livehours,regtime,lastviewtime,lastactiontime,lastpubtime,timezone="","","","","",""
    for li in liarr.items():
        if '在线时间' in li.text():
            livehours = li.text().replace('在线时间','').strip()
        if '注册时间' in li.text():
            regtime = li.text().replace('注册时间','').strip()
        if '最后访问' in li.text():
            lastviewtime = li.text().replace('最后访问','').strip()
        if '上次活动时间' in li.text():
            lastactiontime = li.text().replace('上次活动时间','').strip()
        if '上次发表时间' in li.text():
            lastpubtime = li.text().replace('上次发表时间','').strip()
        if '所在时区' in li.text():
            timezone = li.text().replace('所在时区','').strip()
    return livehours,regtime,lastviewtime,lastactiontime,lastpubtime,timezone

def split_points(liarr):
    point,prestige,gold=0,0,0
    for item in liarr.items():
        if '积分' in item.text():
            point = get_cnt(item.text())
        if '威望' in item.text():
            prestige = get_cnt(item.text())
        if '金币' in item.text():
            gold = get_cnt(item.text())
    return point,prestige,gold

def remove_html(html):
    import re
    dr = re.compile(r'<[^>]+>',re.S)
    return dr.sub('',html).replace('&#13;','').replace('\r\n','')

if __name__ == '__main__':
    #cds = get_cds()
    #print len(cds)
    #update_cds()
    #print get_lnglat('台灣省桃園縣龜山鄉振興路1089巷15-1號')
    #update_lnglat()
    #gen_json()
    #gen_gexf()
    #get_user(2001)
    #get_user(19999)
    get_users(210587,300000)
