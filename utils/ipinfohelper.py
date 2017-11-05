#coding=utf-8
import sys
import socket
from struct import pack, unpack
# from: http://linuxtoy.org/files/pyip.py
# Blog: http://linuxtoy.org/archives/python-ip.html
# Modified by Demon
# Blog: http://demon.tw/programming/python-qqwry-dat.html

'''用Python脚本查询纯真IP库

QQWry.Dat的格式如下:

+----------+
|  文件头  |  (8字节)
+----------+
|  记录区  | （不定长）
+----------+
|  索引区  | （大小由文件头决定）
+----------+

文件头：4字节开始索引偏移值+4字节结尾索引偏移值

记录区： 每条IP记录格式 ==> IP地址[国家信息][地区信息]

   对于国家记录，可以有三种表示方式：

       字符串形式(IP记录第5字节不等于0x01和0x02的情况)，
       重定向模式1(第5字节为0x01),则接下来3字节为国家信息存储地的偏移值
       重定向模式(第5字节为0x02),

   对于地区记录，可以有两种表示方式： 字符串形式和重定向

   最后一条规则：重定向模式1的国家记录后不能跟地区记录

索引区： 每条索引记录格式 ==> 4字节起始IP地址 + 3字节指向IP记录的偏移值

   索引区的IP和它指向的记录区一条记录中的IP构成一个IP范围。查询信息是这个
   范围内IP的信息

'''
#region
class IPInfo(object):
    '''QQWry.Dat数据库查询功能集合
    '''
    def __init__(self, dbname):
        ''' 初始化类，读取数据库内容为一个字符串，
        通过开始8字节确定数据库的索引信息'''

        self.dbname = dbname
        # f = file(dbname, 'r')

        # Demon注：在Windows下用'r'会有问题，会把\r\n转换成\n
        # 详见http://demon.tw/programming/python-open-mode.html
        # 还有Python文档中不提倡用file函数来打开文件，推荐用open
        f = open(dbname, 'rb')

        self.img = f.read()
        f.close()

        # QQWry.Dat文件的开始8字节是索引信息,前4字节是开始索引的偏移值，
        # 后4字节是结束索引的偏移值。
        # (self.firstIndex, self.lastIndex) = unpack('II', self.img[:8])

        # Demon注：unpack默认使用的endian是和机器有关的
        # Intel x86和AMD64(x86-64)是little-endian
        # Motorola 68000和PowerPC G5是big-endian
        # 而纯真数据库全部采用了little-endian字节序
        # 所以在某些big-endian的机器上原代码会出错
        (self.firstIndex, self.lastIndex) = unpack('<II', self.img[:8])

        # 每条索引长7字节，这里得到索引总个数
        self.indexCount = (self.lastIndex - self.firstIndex) / 7 + 1

    def getString(self, offset = 0):
        ''' 读取字符串信息，包括"国家"信息和"地区"信息

        QQWry.Dat的记录区每条信息都是一个以'\0'结尾的字符串'''

        o2 = self.img.find('\0', offset)
        #return self.img[offset:o2]
        # 有可能只有国家信息没有地区信息，
        gb2312_str = self.img[offset:o2]
        try:
            utf8_str = unicode(gb2312_str,'gb2312').encode('utf-8')
        except:
            return '未知'
        return utf8_str

    def getLong3(self, offset = 0):
        '''QQWry.Dat中的偏移记录都是3字节，本函数取得3字节的偏移量的常规表示
        QQWry.Dat使用“字符串“存储这些值'''
        s = self.img[offset: offset + 3]
        s += '\0'
        # unpack用一个'I'作为format，后面的字符串必须是4字节
        # return unpack('I', s)[0]

        # Demon注：和上面一样，强制使用little-endian
        return unpack('<I', s)[0]

    def getAreaAddr(self, offset = 0):
        ''' 通过给出偏移值，取得区域信息字符串，'''

        byte = ord(self.img[offset])
        if byte == 1 or byte == 2:
            # 第一个字节为1或者2时，取得2-4字节作为一个偏移量调用自己
            p = self.getLong3(offset + 1)
            return self.getAreaAddr(p)
        else:
            return self.getString(offset)

    def getAddr(self, offset, ip = 0):
        img = self.img
        o = offset
        byte = ord(img[o])

        if byte == 1:
            # 重定向模式1
            # [IP][0x01][国家和地区信息的绝对偏移地址]
            # 使用接下来的3字节作为偏移量调用字节取得信息
            return self.getAddr(self.getLong3(o + 1))

        if byte == 2:
            # 重定向模式2
            # [IP][0x02][国家信息的绝对偏移][地区信息字符串]
            # 使用国家信息偏移量调用自己取得字符串信息
            cArea = self.getAreaAddr(self.getLong3(o + 1))
            o += 4
            # 跳过前4字节取字符串作为地区信息
            aArea = self.getAreaAddr(o)
            return (cArea, aArea)

        if byte != 1 and byte != 2:
            # 最简单的IP记录形式，[IP][国家信息][地区信息]
            # 重定向模式1有种情况就是偏移量指向包含国家和地区信息两个字符串
            # 即偏移量指向的第一个字节不是1或2,就使用这里的分支
            # 简单地说：取连续取两个字符串！

            cArea = self.getString(o)
            #o += len(cArea) + 1
            # 我们已经修改cArea为utf-8字符编码了，len取得的长度会有变，
            # 用下面方法得到offset
            o = self.img.find('\0',o) + 1
            aArea = self.getString(o)
            return (cArea, aArea)

    def find(self, ip, l, r):
        ''' 使用二分法查找网络字节编码的IP地址的索引记录'''
        if r - l <= 1:
            return l

        m = (l + r) / 2
        o = self.firstIndex + m * 7
        #new_ip = unpack('I', self.img[o: o+4])[0]

        # Demon注：和上面一样，强制使用little-endian
        new_ip = unpack('<I', self.img[o: o+4])[0]

        if ip <= new_ip:
            return self.find(ip, l, m)
        else:
            return self.find(ip, m, r)

    def getIPAddr(self, ip):
        ''' 调用其他函数，取得信息！'''
        # 使用网络字节编码IP地址
        ip = unpack('!I', socket.inet_aton(ip))[0]
        # 使用 self.find 函数查找ip的索引偏移
        i = self.find(ip, 0, self.indexCount - 1)
        # 得到索引记录
        o = self.firstIndex + i * 7
        # 索引记录格式是： 前4字节IP信息+3字节指向IP记录信息的偏移量
        # 这里就是使用后3字节作为偏移量得到其常规表示（QQWry.Dat用字符串表示值）
        o2 = self.getLong3(o + 4)
        # IP记录偏移值+4可以丢弃前4字节的IP地址信息。
        (c, a) = self.getAddr(o2 + 4)
        return (c, a)

    def output(self, first, last):
        for i in range(first, last):
            o = self.firstIndex +  i * 7
            ip = socket.inet_ntoa(pack('!I', unpack('I', self.img[o:o+4])[0]))
            offset = self.getLong3(o + 4)
            (c, a) = self.getAddr(offset + 4)
            print "%s %d %s/%s" % (ip, offset, c, a)
#endregion

try:
    import requests
except Exception,e:
    import requests
from bs4 import BeautifulSoup
import re

proxiesfile = r'..\out\proxies.txt'

def ProxySpider():
	headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
	for i in range(900):
		url='http://www.xicidaili.com/wt/'+str(i)
		r=requests.get(url=url,headers=headers)
		html = r.text
		#print r.status_code
		soup= BeautifulSoup(html, "html.parser")
		datas=soup.find_all(name='tr',attrs={'class':re.compile('|[^odd]')})
		for data in datas:
			soup_proxy= BeautifulSoup(str(data) , "html.parser")
			proxy_contents=soup_proxy.find_all(name='td')
			ip_org=str(proxy_contents[1].string)
			ip="http://"+ip_org
			port=str(proxy_contents[2].string)
			protocol=str(proxy_contents[5].string)
			ValifyProxy(protocol,ip,port)

def ValifyProxy(protocol='http',ip='',port=0):
    from  urllib2 import  OpenerDirector,Request,ProxyHandler,URLError,HTTPError,BaseHandler
    import urllib2
    import fakerhelper
    proxyheader = ProxyHandler({protocol:"%s:%s" % (ip ,port)})
    proxyopener = urllib2.build_opener(proxyheader)
    baseheader = BaseHandler()
    headers = fakerhelper.GetFakerHeader()
    baseheader.add_parent(headers)
    try:
        testresponse = proxyopener.open("http://www.baidu.com",timeout = 10)
    except:
        print "wrong proxy ip",ip
    else:
        print "correct proxy ip",ip,":",port
        with open(proxiesfile,'ab') as f:
            f.write("%s::%s\n" % (ip , port))

def main():
    i = IPInfo(r'E:\MyProjects\Github\IPProxys\data\QQWry.Dat')
    (c, a) = i.getIPAddr(sys.argv[1])

    # Demon注：如果是在Windows命令行中运行把编码转回gb2312以避免乱码
    if sys.platform == 'win32':
        c = unicode(c, 'utf-8').encode('gb2312')
        a = unicode(a, 'utf-8').encode('gb2312')
    print '%s %s/%s' % (sys.argv[1], c, a)

if __name__ == '__main__':
    #main()
    ProxySpider()
