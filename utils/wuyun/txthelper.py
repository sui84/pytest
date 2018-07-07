#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import re
from utils import timehelper,commonhelper,fhelper
import pandas as pd
import os
import shutil
from multiprocessing import Pool
import traceback

'''
移动小于180M文件到另一个目录 dir_fmove
删除空目录 dir_files -> delete_gap_dir
列出所有子目录下文件路径和大小 dir_files
给目录下单个文件去重(40G->37G) filter_txt
利用正则搜索字符串 search_file
目录下两个两个地合并文件，适用于大些的文件 combine_file
合并同一个目录下的所有文件，适用于小文件 combine_dir
整理文件完后(37G->31G),不同文件下肯定还有很多重复行，暂时没想到办法解决
利用正则表达式搜索字符串，在一个200M的文件里搜索几个也只是8秒，但不知结果怎么分组 search_file
10个多线程搜索字符串,13个字符串费了28分组，而且电脑资源耗费内存，IO太严重,那么跟searchhelper.py的时间差不多 MultiProcessSearch
不用多线程花了1个半小时。。。 search_dir
'''
MaxFileSize = 180*1024*1024
ResultFile = r"D:\DB\txt2\result.txt"
ResultDir = r"D:\DB\txt2\result"
SearchStringFile = r"D:\Temp\FindString2.txt"
SearchDir = r"D:\DB\txt2\search"
PNUM = 8


@timehelper.elapsedtimedeco(True)
def search_file(ifile,strs):
    strs = map(lambda x:'.*'+x.strip()+'.*',strs)
    txtre = r'(\n(%s)\n)' % '|'.join(strs)
    print txtre
    txtrec=re.compile(txtre,re.IGNORECASE)
    #txtre = '(\n?(.*general84016393.*)\n?)'  # slow
    #txtre = '(\n(.*jpv520zx.*|.*general84016393.*)\n)'
    with open(ifile,'r') as f:
        txt=f.read()
    searched = txtrec.findall(txt)
    if len(searched) > 0:
        for s in searched:
            print s[1]
    else:
        print 'Not Found',strs
    return searched

@timehelper.elapsedtimedeco(True)
def search_dir(idir,strfile,ofile):
    files  = dir_files(idir)
    strs = file_lines_no_enter(strfile)
    txtrec=strs_rec(strs)
    lines=[]
    for file,size in files:
        try:
            with open(file,'r') as f:
                txt=f.read()
            searched = txtrec.findall(txt)
            if len(searched) > 0:
                print 'Found in ',file
                lines.append('*'*50+ifile)
                searched = map(lambda x:x[0].lstrip(),searched)
                lines = lines + searched
                print lines
                with open(ofile,'ab') as f:
                    f.writelines(lines)
            else:
                print 'Not Found in ',file
        except Exception,e:
            print 'Error in :',file,'\n',e.message,'\n',traceback.format_exc()

def WrapperSearchInFile(args):
    #多个参数用这层包起来
    return SearchFile(*args)

def SearchFile(ifile,txtrec):
    try:
        with open(ifile,'r') as f:
            txt=f.read()
        searched = txtrec.findall(txt)
        lines = []
        if len(searched)>0:
            print 'Found in ',ifile
            lines.append('*'*50+ifile+'\n')
            for s in searched:
                lines.append(s[0].lstrip())
                print s[1]
            with open(ResultFile,'ab') as f:
                f.writelines(lines)
        else:
            print 'Not Found in ',ifile
    except Exception,e:
        print 'Error in :',ifile,'\n',e.message,'\n',traceback.format_exc()


@timehelper.elapsedtimedeco(True)
def MultiProcessSearch(strs=None):
    pool = Pool(PNUM)
    files  = dir_files(idir)
    args=[]
    if strs==None:
        strs = file_lines_no_enter(SearchStringFile)
    txtrec=strs_rec(strs)
    for file,size in files:
        args.append((file,txtrec))
    pool.map(WrapperSearchInFile,args)


def strs_rec(strs):
    strs = map(lambda x:'.*'+x.strip()+'.*',strs)
    txtre = r'(\n(%s)\n)' % '|'.join(strs)
    print txtre
    txtrec=re.compile(txtre,re.IGNORECASE)
    return txtrec


def dir_fmove(idir,pathfiles,odir):
    files = dir_files(idir,pathfiles)
    for fpath,size in files:
        if size < MaxFileSize and os.path.dirname(fpath) <> odir:  #  200M
            fname = os.path.basename(fpath)
            ofile = os.path.join(odir,fname)
            print "%s -> %s" % (fpath,ofile)
            #shutil.move(fpath,ofile)  # very slow
            if not os.path.exists(ofile):
                os.rename(fpath,ofile)  # ???override cause WindowsError: [Error 183]
            else:
                print "not move"

def dir_dirs(idir,ofile):
    dirarr=[]
    for fpathe,dirs,fs in os.walk(idir):
        for d in dirs:
            dir = os.path.join(fpathe,d)
            dirarr.append(dir)
            if not os.listdir(dir):
              os.rmdir(dir)
              print u'移除空目录: ', dir
    save_file('\n'.join(dirarr),ofile)

def dir_files(idir,ofile=None):
    files=[]
    for fpathe,dirs,fs in os.walk(idir):
      for f in fs:
        fpath = os.path.join(fpathe,f)
        size = os.path.getsize(fpath)
        files.append((fpath,size))
    #fpath=[x[0] for x in files]
    files = sorted(files, key=lambda x: x[1])
    fstr = ''
    for fpath,size in files:
        fstr +=  "%s \t %s\n" % (fpath,size)
    if ofile:
        save_file(fstr,ofile)
    return files

@timehelper.elapsedtimedeco(True)
def combine_file(idir,odir,ofile):
    files = dir_files(idir,ofile)
    for i in range(0,len(files),2):
        file1,size1 = files[i]
        file2,size2 = files[i+1]
        #if size1 > MaxFileSize or size2 > MaxFileSize :
        #    pass
        #else:
            #file1,file2=r"D:\DB\txt2\smallsize\7000001.txt".decode('utf-8'),r"D:\DB\txt2\smallsize\kf0013.csv".decode('utf-8')
        fname = os.path.basename(file2)
        destf = os.path.join(odir,fname)
        lines1,lines2 = file_lines(file1),file_lines(file2)
        lines2[0] = '\n'+lines2[0]
        lines = lines1 + lines2
        nlines = list(set(lines))
        save_file(nlines,destf)
        size = os.path.getsize(destf)
        print "%f\t%s\n%f\t%s\n=> %f\t%s" % (size1/1024.0/1024.0,file1,size2/1024.0/1024.0,file2,size/1024.0/1024.0,destf)

@timehelper.elapsedtimedeco(True)
def combine_dir(idir,odir):
    nlines=[]
    for fname in os.listdir(idir):
        fpath = os.path.join(idir,fname)
        lines = file_lines(fpath)
        nlines = nlines + lines
        print len(nlines)," lines"
    nlines = list(set(nlines))
    dfname = os.path.basename(idir)
    destf = os.path.join(odir,dfname)+'.TXT'
    save_file(nlines,destf)
    print "%s => %f \t %s" % (idir,len(nlines),destf)

def file_lines(fpath):
    with open(fpath,'r') as f:
        lines = f.readlines()
        return lines

def save_file(lines,ofile):
    dirname=os.path.dirname(ofile)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(ofile,'w') as f:
        if type(lines) is list:
            f.writelines(lines)
        else:
            f.write(lines)

def file_lines_no_enter(ifile):
    with file(ifile,'rb') as f:
        data = f.read()
        lines=data.splitlines()
        return lines

@timehelper.elapsedtimedeco(True)
def filter_txt(ifile,ofile):
    #字符串进行去重操作
    with open(ifile,'r') as f:
        lines = f.readlines()
    nlines = list(set(lines))
    '''
    ifile2=r"D:\DB\Splited\1_1.txt"
    with open(ifile2,'r') as f:
        lines2 = f.readlines()
    nlines = list(set(lines+lines2))
    '''
    save_file(nlines,ofile)
    print "ifile(%d) + ifile2(%d) => ofile(%d) lines" % (len(lines),0,len(nlines))

@timehelper.elapsedtimedeco(True)
def filter_txt2(ifile,ofile):
    #pandas : take more time
    with open(ifile,'r') as f:
        lines = f.readlines()
    df=pd.DataFrame({"line":lines})
    result=df.drop_duplicates()
    with open(ofile,'w') as f:
        f.writelines(result.line.tolist())


if __name__ == '__main__':
    ifile=r"D:\DB\Splited\1_1.txt"
    ifile=r"D:\DB\txt\库1.txt".decode('utf-8')
    ofile=r"d:\temp\test.txt"
    idir = r"D:\DB\txt2"
    odir = r"D:\DB\txt2\smallsize"
    dir_dirs(r"D:\DB\txt2",ofile)
    #delete_gap_dir(idir)
    #dir_files(r"D:\DB\txt2",ofile)
    #dir_fmove(idir,ofile,odir)
    #combine_file(r"D:\DB\txt2\smallsize",r"D:\DB\txt2\combine",ofile)
    #combine_dir(r"D:\DB\txt2\combine\dir23",r"D:\DB\txt2\combine")
    #filter_txt(ifile,ofile)
    #filter_txt2(ifile,ofile)
    #search_file(r"D:\DB\txt2\search\1_2.txt",['gta552003@yahoo.com.cn','hdnsvhzqa859184@qq.com','jpv520zx'])
    MultiProcessSearch()
    #search_dir(SearchDir,SearchStringFile,ResultFile)
