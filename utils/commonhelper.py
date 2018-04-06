#encoding=utf-8
import urlparse
import os
import urllib
import whois
import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import commands
import subprocess
import os.path
import hashlib
import html
import base64
import json
import socket
from tqdm import tqdm


def GetFullUrl(url1,url2):
    if not url1.endswith('/'):
        url1 = url1 +'/'
    newurl = urlparse.urljoin(url1,url2)
    return newurl
        
def GetDstPath(dstdir,dirfname):
    print dstdir,dirfname
    dstfpath=""
    if os.path.isdir(dstdir):
        fname = os.path.basename(dirfname)
        dstfpath = os.path.join(dstdir,fname)
    elif os.path.isfile(dstdir):
        dstfpath = dstdir
    return dstfpath

def SetToDict(keys):
    # keys = {'a','b','c'} => {'a':[],'b':[],'c':[]}
    value = []
    d = dict.fromkeys(keys,value)
    return d

def StrToDict(dictstr):
    #也适用于list字符串转换成list
    d = eval(a)
    return d
    
def StrToDict2(dictstr):
    exec ("d=" + a)
    return d

def UrlEncode(str):
    # str = 'name = ~nowamagic+5'  return name%20%3D%20%7Enowamagic%2B5
    newstr = urllib.quote(str)
    return newstr

def UrlDecode(str):
    newstr = urllib.unquote(str)
    return newstr

def UrlEncodePlus(str):
    # str = 'name = ~nowamagic+5'  return name+%3D+%7Enowamagic%2B5
    newstr = urllib.quote_plus(str)
    return newstr

def UrlDecodePlus(str):
    newstr = urllib.unquote_plus(str)
    return newstr

def DictEncode(dictobj):
    # dictobj : { 'name': 'nowamagic-gonn', 'age': 200 } return age=200&name=nowamagic-gonn
    newstr = urllib.urlencode(dictobj)
    return newstr

def PathToUrl(path):
    # path :  r'd:/a/b/c/23.php' return ///D://a/b/c/23.php
    newstr = urllib.pathname2url(path)
    return newstr

def UrlToPath(url):
    # url : ///D://a/b/c/23.php return D:/a/b/c/23.php
    newstr = urllib.url2pathname(url)
    return newstr

def WhoIs(domain):
    # baidu.com 需要linux安装whois ,window平台用不了
    whoisData = whois.query("baidu.com")
    print whoisData
    return whoisData

def SaveWinCommandResult(batfile,ofile):
    #执行bat文件，结果保存
    with open(batfile) as f:
        batchcmd = f.read()
    SaveWinCommandResult(batchcmd,ofile)

def SaveWinCommandResult(batchcmd,ofile):
    '''
    在window下执行多个命令,一定要有exit,不然就一直停在那里
    batchcmd = b"""\
    set TEST_VAR=Hello World
    set TEST_VAR
    echo %TEST_VAR%
    exit
    """
    stdout,stderr=os.system('dir c:\\')
    如果没有stderr总是返回1,然而这样依然返回不了结果
    '''
    cmdline = ["cmd", "/q", "/k", "echo off"]
    cmd = subprocess.Popen(cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    cmd.stdin.write(batchcmd)
    cmd.stdin.flush() # Must include this to ensure data is passed to child process
    result = cmd.stdout.read()
    #print result
    #UnicodeDecodeError: 'ascii' codec can't decode byte 0xd5 in position 2: ordinal not in range(128)
    #print(result.decode())
    #返回结果会报错，写到文件不会报错，但会是乱码。。。不知怎么解决，暂时先这样吧
    with open(ofile, 'a') as f:
         f.write(result.decode())
    #return result

def GetCommandResult(cmsstr="ls"):
    # 只有linux平台起作用
    cmdresult =  commands.getoutput(cmsstr)
    return cmdresult

def GetPadString(num,len):
    #数字字符串前面补0
    nnum=str(num).zfill(len)
    return nnum

def CheckDir(dirname, filenames ):
    print 'Directory',dirname
    for filename in filenames:
        #print ' File',filename
        fpath = os.path.join(dirname, filename)
        print fpath
        files.append(fpath)

def GetDirAndFiles(dirpath):
    #列出所有子目录和文件
    global files
    files=[]
    os.path.walk(dirpath, CheckDir, None)
    print u'总共%d个文件' % len(files)
    return files

def GetDirFiles(dirpath):
    #只列出文件
    files=[]
    for fpathe,dirs,fs in os.walk(dirpath):
      for f in fs:
        files.append(os.path.join(fpathe,f))
    return files

def ExecuteCmd(cmdstr):
    # 阻塞执行命令：获取所有子目录和文件
    # cmdstr = r"dir D:\DB\txt /s/-b >d:\temp\filelist.txt"
    print cmdstr
    result = os.system(cmdstr)
    if result == False:
        print "Success!"
    else:
        print "Failed!"

def ExecuteCmdWithSubProcess(cmdlist):
    import subprocess
    #r=subprocess.call(['ping','www.baidu.com'])
    r=subprocess.call(cmdlist)

def Str2Unicode(str):
    #str = "\\u7f8e\\u56fd"
    unicodestr = str.decode("unicode-escape")
    print unicodestr
    return unicodestr

def Unicode2Str(unicodestr):
    #unicodestr = u"美国"
    str = unicodestr.encode("unicode-escape")
    print str
    return str

def Base64Encode(content):
    return base64.b64encode(bytes(content))

def Base64Decode(content):
    return base64.b64decode(bytes(content))

def Base64URLEncode(content):
    return base64.urlsafe_b64encode(bytes(content))

def Base64URLDecode(content):
    return base64.urlsafe_b64decode(bytes(content))

def URLEncode(content):
    return urllib.parse.quote(content, safe='')

def URLDecode(content):
    return urllib.parse.unquote(content)

def URLJSONEncode(content):
    json_content = json.loads(content)
    return urllib.parse.urlencode(json_content)

def URLJSONDecode(content):
    return str(urllib.parse.parse_qs(content))

def HTMLEncode(content):
    return html.escape(content)

def Dec2HEX(content):
    figures = content.split(' ')
    result = ' '
    figure_list = []
    for figure in figures:
        figure_list.append(str(hex(int(figure))))
    return result.join(figure_list)

def Hex2Dec(content):
    figures = content.split(' ')
    result = ' '
    figure_list = []
    for figure in figures:
        figure_list.append(str(int(figure, 16)))
    return result.join(figure_list)

def MD5(content):
    return hashlib.md5(bytes(content)).hexdigest()

def SHA1(content):
    return hashlib.sha1(bytes(content)).hexdigest()

def SHA256(content):
    return hashlib.sha256(bytes(content)).hexdigest()

def SHA384(content):
    return hashlib.sha384(bytes(content)).hexdigest()

def SHA512(content):
    return hashlib.sha512(bytes(content)).hexdigest()

def RemoveDuplicate(l=['8','7','7','5']):
    #去重并保留原来顺序
    result=list(set(l))
    result.sort(key=l.index)
    return result

def GetCurrentIP(url="http://ip.chinaz.com/getip.aspx"):
    r=requests.get(url)
    return r.text

def Progressbar():
    pbar = tqdm(["a", "b", "c", "d"])
    for char in pbar:
        pbar.set_description("Processing %s" % char)

'''
sys.stdout重定向
将一个可写对象(如file-like对象)赋给sys.stdout，可使随后的print语句输出至该对象。重定向结束后，应将sys.stdout恢复最初的缺省值，即标准输出。

简单示例如下：

import sys
savedStdout = sys.stdout  #保存标准输出流
with open('out.txt', 'w+') as file:
    sys.stdout = file  #标准输出重定向至文件
    print 'This message is for file!'

sys.stdout = savedStdout  #恢复标准输出流
print 'This message is for screen!'
'''

