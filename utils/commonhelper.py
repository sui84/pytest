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
        
def StrToDict(dictstr):
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
