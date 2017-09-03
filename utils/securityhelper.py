#encoding=utf-8
from pyquery import PyQuery as pq
import requests
import hashlib
import md5
import fakerhelper
import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class SecurityHelper(object):
    def __init__(self):
        self.md5url='http://www.cmd5.com/'
        ua=fakerhelper.GetFakerData(type='useragent')
        self.headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                                            ,'Accept-Encoding':'gzip,deflate,sdch'
                                            ,'Accept-Language':'zh-CN,zh;q=0.8'
                                            ,'User-Agent': ua
                                            ,'Content-Type':'application/x-www-form-urlencoded'}
        self.mode = AES.MODE_CBC

    def Encrypt(self,text,key):
        # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
        # 不加b'0000000000000000' 报错：IV must be 16 bytes long
        # key必须是16的倍数，不然报错：AES key must be either 16, 24, or 32 bytes long
        cryptor = AES.new(key, self.mode,b'0000000000000000')
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    def Decrypt(self, text,key):
        #解密后，去掉补足的空格用strip() 去掉
        #cryptor = AES.new(self.key, self.mode, self.key)
        cryptor = AES.new(key, self.mode,b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

    def GetEncryptMd5(self,str):
         m=hashlib.md5()
         m.update(str)
         md5str = m.hexdigest()
         return md5str

    def GetEncryptMd5ByMd5(self,str):
         m=md5.new()
         m.update(str)
         md5str = m.hexdigest()
         return md5str

    def GetDecryptMd5(self,md5str):
        r = requests.get(self.md5url, headers=self.headers)
        cookies=r.headers["set-cookie"]
        s = requests.Session()
        md5data={"__EVENTTARGET":""
,"__EVENTARGUMENT":""
,"__VIEWSTATE":r"e/KhnxcOVaIW71DMM/fQfPsrkhm6d+avJB4jwbKiO0KVYyQ2PAWYI5k6tcrNOtNd3cxvHspoeYYG77H40CgGmc3l9lnG3f0qhQlV81k5WKFR08OGRjmH5cnx6KxmbFlt7mh8Tek3njkLqopqMaIodJRTADtMKERz6F4KTFljoDwb89g/IPkzJnMIixfP1EfrDcnL34kVL8QppJrNak0jFu7PHa522VCLZW8Q72fgia3QcBWXtPNbNVlGqLNJDd5qKXq5MLlB27pml6ANLufyeGHSehdj3fXyMhtiA4OARyj400rk4E23tV8M1KdDvtmayJIRkt5ZLVzGkt1bZmsoFpB8zepYI0jr3wn3U66L/VM3mv2Ymzii1fC/JJTWpVbeCacpg+EKFoQ31g1hjVHhsm8KUtDdg7hjSBSZ+K3ieKzIAXBG4Qxe3+l5gAA5QFzp+SXSXWuTmmFCtRhJUCQxcr172ZHbbSVqYGp1keq0/iTmWAyNRxjBDzwOSnj0zbsEdy9TJpw5fzSn2dBzlo6eXmHdWgpA5vdkjYmZ41xXkDwyV7OwZopt8xfLmH0HeKD/mUuyP+BnM1l6EAVkie3RaZFQulo+VSNcTcPj8OX77QEirhe/30+GU8M57CGPizONL3Ot9aTIDp127azZRkY/6xhDl1rrguerKPIDzRISdVMVv0NJmk4lxpnKjFyODili+pPIbawJ47H80fSVK9KONl+WUMnAg1GCEiQ/iFtQqlMXjhibo/H5oNttlJd/KhBOwSUOr1ny1oRgWSbKgXpv/qMlZDtRhrw5eqJHjEXfSfLSkczPQ9oLXlHqbdjoIhiqrpjXkKHm9BnS1ADtt8GkMsscj9L2FrfmEJZTwSb9yPE+e0whKWdeJmKACN/03JDQxGujHgBZ+2FMiWB4kJmddzqLhjxB21Q9MdBr+PufD8gdhBgntcG4TbocvUIEzyIosoiLUg6JiMVfMHD4XrRvIcGJfUOe1hh0ayHo4d6+oVCKOpi5DKVrsdbSRTwlJSOVRJViFfFqDOMLWr+iGdldd78e+OYMPL+Tjq9Ads0VO6LQGVyc8NBBNgwX0nrL89GvswijQYsIGlQEf8A/8id0Ne7qBJSrnBFV7e2OjYnisQlbnVKXio5HoMejg/NN2I1r53YLiIrrXWm1+Huo2nDa3WCIkYRE2PowwyZVwBNswDso5+Gdw2+34tgbOK6l4NFSMgUagW478SnHyXCWYmpuSkiwyu0hcYgqQ6l+mZ3CefrTyXDVeLDeBQzWf4wH6rO9BPvS5yNF97wwH1yRWgp89Ag86mlrLLsgdcfYHw8RQW1xuzTtUe8m8tGJIUN6qf0gPF2ylKGhalzVaGD+Vz1Hz6kee4/wU8YrAoeFiH9oELFUUbazyPI0vt45X0anbCg6WBEyjfaekDtTp/5z1Fbvvc3GXLRjOMhYkqVSs0vk69VgNMzg"
,"__VIEWSTATEGENERATOR":"CA0B0334"
,"ctl00$ContentPlaceHolder1$TextBoxInput":md5str
,"ctl00$ContentPlaceHolder1$InputHashType":"md5"
,"tl00$ContentPlaceHolder1$Button1":u"查询"
,"ctl00$ContentPlaceHolder1$HiddenField1":""
,"ctl00$ContentPlaceHolder1$HiddenField2":"4CLI+LhikvJd2akMl/XItk9ZgAaPa3zmm9k5z3V3Bkl6bI3zhdPiG+EIm+sRM0vN"}
        r=s.post(url=self.md5url,data=md5data)# ,cookies=cookies)  not work!!
        d=pq(r.text.encode('utf-8','ignore'))
        answer=d('#ctl00_ContentPlaceHolder1_LabelAnswer').text()
        answer=answer.replace(u'[添加备注]','')
        return answer

if __name__ == '__main__':
    mh = SecurityHelper()
    str="ed"
    md5str=mh.GetEncryptMd5(str)
    #md5str="b5f3729e5418905ad2b21ce186b1c01d"
    print md5str
    #print mh.GetDecryptMd5(md5str)
    # key必须为16的倍数
    key="testtesttesttest"
    str= "ed"
    estr = mh.Encrypt(str,key)
    print str,estr
    dstr = mh.Decrypt(estr,key)
    print estr,dstr
