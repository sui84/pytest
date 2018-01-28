#encoding=utf-8
import string
import pickle
import json
import re
import chardet
import binascii
import struct

#S.split(str,'')
#S.join(list,'')


class StrHelper(object):
    def __init__(self):
        self.splitchars=re.compile(r",|，| |/|")

    def ReplaceStringFile(self,fpath,*args):
        with  open(fpath,'r') as f:
            str = f.read()
        # pass args will cause error : takes exactly 2 arguments (4 given)
        nstr = self.ReplaceString(str,*args)
        return nstr

    def ReplaceString(self,str,*args):
        # xmldata = re.sub('<web:startCity>(.*?)\</web:startCity>','<web:startCity>%s</web:startCity>' % fcitycode,xmldata)
        nstr = str % (args)
        return nstr

    def ReplaceListsString(self,str,lists):
        nlists=[(lambda x:str % x )(x) for x in lists]
        return nlists

    def SplitString(self,str):
        c=self.splitchars.split(str)
        return c

    def SerializeString(self,obj):
        dumpsed = pickle.dumps(obj)
        return dumpsed

    def SerializeToFile(self,obj,ofile):
        dumpsed = pickle.dumps(obj)
        pickle.dump(obj,open(ofile,'w'))

    def Deserialize(self,dumpsed):
        loadsed = pickle.loads(dumpsed)
        return loadsed

    def DeserializeFromFile(self,ifile):
        loadsed = pickle.load(open(ifile,'r'))
        return loadsed

    def Jsonstr2Obj(self,jsonstr):
        obj =json.loads(jsonstr)
        return obj

    def Obj2JsonStr(self,obj):
        jsonstr =json.dumps(obj)
        return jsonstr

    def Trim(self,str):
        return str.strip()

    def ReplaceIgnorecase(self,istr,str,rstr):
        #replace 函数区分大小写
        #istr 源字符串 , str 查找字符串 , rstr 替换字符串
        #str和rstr都不能以\结尾，不然会报错 SyntaxError: invalid syntax
        reg = re.compile(re.escape(str), re.IGNORECASE)
        ostr = reg.sub(rstr, istr)
        return ostr

    def Convert2UTF8(self,str):
        # detect unicode character cause error : TypeError: Expected object of type bytes or bytearray, got: <type 'unicode'>
        ostr=unicode(str).encode('utf8')
        return ostr

    def ConvertToUTF8(self,str):
        #先判断字符编码 for example 'iso-8859-1'
        #但是如果本身是unicode，会报错TypeError: Expected object of type bytes or bytearray, got: <type 'unicode'>
        cset = chardet.detect(str).get('encoding')
        ostr=str.decode(cset).encode('utf8')
        return ostr

    def ConvertToUnicode(self,str):
        cset = chardet.detect(str).get('encoding')
        ostr=unicode(str,cset)
        return ostr

def example(express, result=None):
    if result == None:
        result = eval(express)
    print(express, ' ==> ', result)


if __name__ == '__main__':
    '''
    str='\x31\x32\x61\x62'
    bytes(str)
    '12ab'
    '''

    print '整数之间的进制转换:'
    print "10进制转16进制",example("hex(16)")
    print "16进制转10进制",example("int('0x10', 16)")
    print("类似的还有oct()， bin()")

    print('\n-------------------\n')

    print('字符串转整数:')
    print "10进制字符串",example("int('10')")
    print "16进制字符串",example("int('10', 16)")
    print "16进制字符串",example("int('0x10', 16)")

    print('\n-------------------\n')

    print('字节串转整数:')
    print "转义为short型整数",example(r"struct.unpack('<hh', bytes(b'\x01\x00\x00\x00'))")
    print "转义为long型整数",example(r"struct.unpack('<L', bytes(b'\x01\x00\x00\x00'))")

    print('\n-------------------\n')

    print('整数转字节串:')
    print "转为两个字节",example("struct.pack('<HH', 1,2)")
    print "转为四个字节",example("struct.pack('<LL', 1,2)")

    print('\n-------------------\n')

    print('字符串转字节串:')
    print '字符串编码为字节码',example(r"'12abc'.encode('ascii')")
    print '数字或字符数组',example(r"bytes([1,2, ord('1'),ord('2')])")
    print '16进制字符串',example(r"bytes().fromhex('010210')")
    print '16进制字符串', example(r"bytes(map(ord, '\x01\x02\x31\x32'))")
    print '16进制数组', example(r'bytes([0x01,0x02,0x31,0x32])')

    print('\n-------------------\n')

    print('字节串转字符串:')
    print '字节码解码为字符串', example(r"bytes(b'\x31\x32\x61\x62').decode('ascii')")
    print '字节串转16进制表示,夹带ascii', example(r"str(bytes(b'\x01\x0212'))[2:-1]")
    print '字节串转16进制表示,固定两个字符表示',example(r"str(binascii.b2a_hex(b'\x01\x0212'))[2:-1]")
    print '字节串转16进制数组',example(r"[hex(x) for x in bytes(b'\x01\x0212')]")


    print('\n===================\n')


