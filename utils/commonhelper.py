#encoding=utf-8
import urlparse
import os



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
