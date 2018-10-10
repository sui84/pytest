#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import re
import wget, tarfile
import os
'''
用'r'读到文本中的ESC时候会中止，读不全
用'rU'就可以了???
以 'U' 标志打开文件, 所有的行分割符通过 Python 的输入方法(例#如 read*() )，返回时都会被替换为换行符\n. ('rU' 模式也支持 'rb' 选项)
调用seek指向开头fd.seek(0)
按字节读取f.read(1024) # 每次读取 1024 个字节（即 1 KB）的内容
'''

log_file = r"D:\DB\log\bettercap.log"
url_file = r"D:\DB\log\url.txt"
tre=' GET.*?(.*?\\.img|.*?\\.jpg|.*?\\.pad|.*?\\.txt|.*?\\.webp|.*?\\.tiff|.*?\\.raw|.*?\\.png|.*?\\.gif|.*?\\.swf|.*?\\.mp4|.*?\\.jpeg|.*?\\.deb|.*?\\.pdf|.*?\\.doc|.*?\\.exe|.*?\\.avi|.*?\\.mp3|.*?\\.docx|.*?\\.xls|.*?\\.xlsx|.*?\\.xml|.*?\\.ppt)'
trec=re.compile(tre,re.IGNORECASE)
image_dir = r"D:\DB\log\image"

def get_url(ifile,ofile):
    with open(ifile,'rU') as f:
        txt = f.read()
        searched=trec.findall(txt)
        nlines = list(set(searched))
        with open(ofile,'a') as f:
            for s in nlines:
                f.write('http://'+s.strip()+'\n')
    print len(searched),'=>',len(nlines)

def get_file(ifile,odir):
    i = 0
    with open(ifile,'r') as f:
        for url in f:
            try:
                url = url.strip()
                i += 1
                print url
                fp,fn=os.path.split(url)
                #ofile = os.path.join(odir,os.path.basename(url))
                #ofile = os.path.join(odir,fn)
                fn,ext = os.path.splitext(fn)
                ofile = os.path.join(odir,str(i)+ext)
                #ofile = odir + '\\'+ str(i)+ext
                print ofile
                if not os.path.exists(ofile):
                    wget.download(url,ofile)
            except Exception,e:
                import time,traceback
                print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()


if __name__ == '__main__':
    #get_url(log_file,url_file)
    #get_file(log_file)
    get_file(url_file,image_dir)
