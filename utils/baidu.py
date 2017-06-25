# -*- coding: utf8 -*-
import urllib2
import urllib
import cookielib
import re
import bs4
import json
import time
import Cookie
import random
import datetime
#import syslog
#import requests
URL_BAIDU_INDEX = u'http://www.baidu.com/';
#https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true 也可以用这个
URL_BAIDU_TOKEN = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login';
URL_BAIDU_LOGIN = 'https://passport.baidu.com/v2/api/?login';
SAVE_FILE = 'D:\\bduhis.txt';
SAVE_JFILE = 'D:\\json.txt';
SAVE_CFILE = 'D:\\cookie.txt';
#设置用户名、密码
username = '';
password = '';
#设置cookie，这里cookiejar可自动管理，无需手动指定
#cj = cookielib.CookieJar();
filename = 'cookie.txt'
cj = cookielib.MozillaCookieJar(SAVE_CFILE);

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
urllib2.install_opener(opener);
#print cj;
reqReturn = urllib2.urlopen(URL_BAIDU_INDEX);
#cj.set_cookie(make_cookie('testname','testvalue' )) 
'''更改cookie不成功
c=Cookie.SimpleCookie();
c["Manageopen"]="cards";
c['Manageopen']['expires'] = 0;
c['Manageopen']['path'] = "/";
c['Manageopen']['domain'] = ".domain.com";
c['Manageopen']['secure'] = "";
cj.set_cookie(c["Manageopen"]) ;
'''
print cj;
cj.save(ignore_discard=True, ignore_expires=False)

#获取token,
tokenReturn = urllib2.urlopen(URL_BAIDU_TOKEN);
matchVal = re.search(u'"token" : "(?P<tokenVal>.*?)"',tokenReturn.read());
tokenVal = matchVal.group('tokenVal');
#构造登录请求参数，该请求数据是通过抓包获得，对应https://passport.baidu.com/v2/api/?login请求

postData = {
'username' : username,
'password' : password,
'u' : 'https://passport.baidu.com/',
'tpl' : 'pp',
'token' : tokenVal,
'staticpage' : 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
'isPhone' : 'false',
'charset' : 'utf-8',
'callback' : 'parent.bd__pcbs__ra48vi'
};
postData = urllib.urlencode(postData);
#发送登录请求
loginRequest = urllib2.Request(URL_BAIDU_LOGIN,postData);
loginRequest.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');
loginRequest.add_header('Accept-Encoding','gzip,deflate,sdch');
loginRequest.add_header('Accept-Language','zh-CN,zh;q=0.8');
loginRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');
loginRequest.add_header('Content-Type','application/x-www-form-urlencoded');

sendPost = urllib2.urlopen(loginRequest);
#查看贴吧个人主页 ，测试是否登陆成功，由于cookie自动管理，这里处理起来方便很多
#http://tieba.baidu.com/home/main?un=XXXX&fr=index 这个是贴吧个人主页，各项信息都可以在此找到链接
#teibaUrl = 'http://tieba.baidu.com/f/like/mylike?v=1387441831248'
# http://i.baidu.com/my/history
# http://map.baidu.com/ 
#http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc3&qt=fav&mode=get&type=favdata&limit=100&lastver=0&t=1481726657277
#teibaUrl = 'http://i.baidu.com/my/historylogin'
teibaUrl = 'http://i.baidu.com/login/historyCheck/?autoLogin=true'
content = urllib2.urlopen(teibaUrl).read();
#print content;
teibaUrl = 'http://i.baidu.com/history/list'
content = urllib2.urlopen(teibaUrl).read();
content = content.decode('utf-8').encode('GB18030');
print content;
teibaUrl = 'http://map.baidu.com/?qt=ssn&t=1482059818916'
content2 = urllib2.urlopen(teibaUrl).read();
content2 = content2.decode('utf-8').encode('GB18030');
print content2;
'''1. save to html file
def cbk(a, b, c):  
	#回调函数 
	#@a: 已经下载的数据块 
	#@b: 数据块的大小 
	#@c: 远程文件的大小 
	per = 100.0 * a * b / c  
	if per > 100:  
		per = 100  
	print '%.2f%%' % per 
urllib.urlretrieve('http://www.cmfish.com/bbs/forum.php','D:\\baidu1.html',cbk);
'''

def save(filename, contents): 
  fh = open(filename, 'w') 
  fh.write(contents) 
  fh.close() 
'''2. save to txt file
t = json.dumps(content, ensure_ascii=False);
hjson = json.loads(content, encoding='utf-8');
#t2=content.decode('utf-8');
#print hjson['data']['list'][0]['query'];
print hjson;
arr = hjson['data']['list']
tdata = 'Start----------------------------\nTime:'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' Total:'+str(len(arr))+':\n';
for elem in arr:
	data = str(elem['ts'])+','+elem['query']+','+str(len(elem['clicks']));
	if len(elem['clicks'])>0:
		try:
			for cd in elem['clicks']:
				data = data + ','+str(cd['title'])+','+str(cd['url']);		
		except Exception,e:
		    tdata = tdata + 'Error:'+str(e)+'\n';
	tdata = tdata + data+'\n';		
print tdata;
tdata = tdata + 'End----------------------------\n';
save(SAVE_FILE, tdata.encode('gbk')) ;
'''
hjson = json.loads(content, encoding='utf-8');
save(SAVE_JFILE, content.encode('utf-8')) ;
# 3. save to mongodb
from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)
db = client["Collections"]#数据库名
table=db['his']#表名
table.save(hjson)
hjson2 = json.loads(content2, encoding='utf-8');
table.save(hjson2)
#table.insert({'id':'1','name':'cnki'})


'''
#解析数据，用的BeautifulSoup4，感觉没有jsoup用的爽
soup = bs4.BeautifulSoup(content);
#print soup.prettify();
list = soup.findAll('a',attrs={"href":re.compile(r"^http:")});
#list = soup.findAll(name='a',attrs={'href':re.compile(r"kw="),'title':re.compile(r".")}) ;
list = list[1:len(list)];
careTeibalist = [];
print '贴吧链接\\t吧名\\t等级';
print  len(list);
for elem in list:
	soup1 = bs4.BeautifulSoup(str(elem));
	print 'http://tieba.baidu.com/'+elem['href']+'\\'+elem['title'];
'''
