#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import re
import os
import shutil
from multiprocessing import Pool
import traceback
import dirhelper
import time
import logging

'''
给目录下单个文件去重(40G->37G) filter_txt
利用正则搜索字符串 search_file
整理文件完后(37G->31G),不同文件下肯定还有很多重复行，可以用布隆过滤法解决
利用正则表达式搜索字符串，在一个200M的文件里搜索几个也只是8秒，但不知结果怎么分组 search_file
10个多线程搜索字符串,13个字符串费了28分组，而且电脑资源耗费内存，IO太严重,那么跟searchhelper.py的时间差不多,瓶颈在于没有那么大内存的电脑 MultiProcessSearch
不用多线程花了1个半小时。。。 search_dir
读一个200M的文本，实际耗费的内存大概280M python -m cProfile ./wuyun/txthelper.py -o result
用mmap没办法一次性读取接近1G的文本文件 filter_bigfile2
可以逐行读取大文件，1.7G大小也就4分钟，资源占用也不多，内存才耗88M。。。不动怎么那么少 filter_bigfile
若是将文本导入数据库，将占据好几倍的大小 Bulk  insert  TEXT From  'D:\temp\data.txt' With ( rowterminator='\n')
布隆过滤大文件，速度超级慢，200M的文件花了15分钟，生成的bloom对象跟size有关,仅需要4分1的空间 bloom_filter
'''

ResultFile = r"D:\DB\txt2\result.txt"
ResultDir = r"D:\DB\txt2\result"
SearchStringDir = r"D:\DB\txt2\keystr"
SearchDir = [r"D:\DB\txt2\big\tianya"]
LogFile = r"D:\DB\txt2\log.txt"
PNUM = 8


def cur_time(fmt='%Y/%m/%d %H:%M:%S'):
    return time.strftime(fmt)

def log_deco(logfile=True):
    def _deco(func):
        def wrapper(*args,**kwargs):
            startTime = time.time()
            func(*args,**kwargs)
            endTime = time.time()
            msecs = (endTime - startTime) * 1000
            timeinfo = "%s -> elapsed time: %.2f sec %.2f min" % (func.__name__,msecs/1000.0,msecs/(60*1000.0))
            if logfile:
                logger = create_logger(LogFile)
                logger.info(timeinfo)
            else:
                print timeinfo
        return wrapper
    return _deco

def create_logger(logpath):
    logger = logging.getLogger("testlogger")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logpath)
    fmt = '[%(asctime)s - %(name)s - %(levelname)s %(process)d %(processName)s %(thread)d %(threadName)s] %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)
    return logger

Logger = create_logger(LogFile)

@log_deco(False)
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

@log_deco(False)
def search_dir(idir,strfile,ofile):
    files  = dirhelper.dir_files(idir)
    strs = dirhelper.file_lines_no_enter(strfile)
    txtrec=strs_rec(strs)
    lines=[]
    for file,size in files:
        try:
            print 'start check ',ifile , '...'
            with open(file,'rb') as f:
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
        except Exception,e:
            print 'Error in :',file,'\n',e.message,'\n',traceback.format_exc()

def WrapperSearchInFile(args):
    #多个参数用这层包起来
    return SearchFile(*args)

def SearchFile(ifile,strs,ofile):
    try:
        Logger.info('Start scan [%s]'% (ifile))
        i=0
        with open(ifile,'r') as f:
            for line in f:
                i+=1
                if i % 1000000 == 0:
                    Logger.info('Scaning [%s] Lines [%d]'% (ifile,i))
                for str in strs:
                    if str in line:
                        Logger.info('Found in lines [%d] in [%s]'% (i,ifile))
                        with open(ofile,'ab') as f:
                            f.write("[%s][%d][%s][%s]\n" % (ifile,i,str,line.strip()))
        Logger.info('End scan [%s] total lines [%d] size [%d]'% (ifile,i,os.path.getsize(ifile)))
    except Exception,e:
        print 'Error in :',ifile,'\n',e.message,'\n',traceback.format_exc()


@log_deco(True)
def MultiProcessSearch(idirs=SearchDir,keydirs =SearchStringDir,ofile=ResultFile,strs=None):
    pool = Pool(PNUM)
    files,args,strs = [],[],[]
    for idir in idirs:
        files  = files + dirhelper.dir_only_files(idir)
    Logger.info(keydirs)
    keyfiles=dirhelper.dir_only_files(keydirs)
    for file in keyfiles:
        strs = strs + dirhelper.file_lines_no_enter(file)
    if len(files) == 0 or len(strs)==0:
        Logger.info("No need Scan")
        exit(0)
    info = "SearchDir : %s\nSearchStringDir : %s" % (str(SearchDir),str(SearchStringDir))
    Logger.info(info)
    #txtrec=strs_rec(strs)
    for file in files:
        args.append((file,strs,ofile))
    pool.map(WrapperSearchInFile,args)
    for file in keyfiles:
        fname = time.strftime('%Y%m%d%H%M%S')+".TXT"
        os.rename(file,os.path.join(SearchStringDir,"bk",fname))
    Logger.info("[%s]End Scan" % cur_time())


def strs_rec(strs):
    strs = map(lambda x:'.*'+x.strip()+'.*',strs)
    txtre = r'(\n(%s)\n)' % '|'.join(strs)
    #print txtre
    txtrec=re.compile(txtre,re.IGNORECASE)
    return txtrec


@log_deco(False)
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
    dirhelper.save_file(nlines,ofile)
    print "ifile(%d) + ifile2(%d) => ofile(%d) lines" % (len(lines),0,len(nlines))

@log_deco(False)
def filter_txt2(ifile,ofile):
    import pandas as pd
    #pandas : take more time
    with open(ifile,'r') as f:
        lines = f.readlines()
    df=pd.DataFrame({"line":lines})
    result=df.drop_duplicates()
    with open(ofile,'w') as f:
        f.writelines(result.line.tolist())


from memory_profiler import profile
@profile
@log_deco(False)
def filter_bigfile(ifile,ofile):
    i=0
    lines=[]
    print 'start check ',ifile , '...'
    with open(ifile, 'rb') as f:
        for line in f:
            i+=1
            lines.append(line)
            if i % 100000 == 0:
                print 'lines :',i
    print 'end check lines :',i
    '''
    import pickle
    with open(ofile', 'wb') as f:
        pickle.dump(lines, f)
        f.close()
    '''
    with open(ofile, 'wb') as new_file:
        new_file.writelines(sorted(list(set(lines))))


@profile
@log_deco(False)
def filter_bigfile(ifile,ofile):
    i=0
    lines=[]
    with open(ifile, 'rb') as f:
        for line in f:
            i+=1
            lines.append(line)
    print i
    '''
    import pickle
    with open(ofile', 'wb') as f:
        pickle.dump(lines, f)
        f.close()
    '''
    with open(ofile, 'wb') as new_file:
        new_file.writelines(sorted(list(set(lines))))

from pybloom import BloomFilter
import pickle
@profile
@log_deco(False)
def bloom_filter(ifile,ofile,dupfile,blofile,maxsize=99999999):
    blf = BloomFilter(capacity=maxsize, error_rate=0.001)
    with open(ifile, 'rb') as f:
        lines=f.readlines()
    lines_len=len(lines)
    for line in lines:
        if line in blf:
           lines.remove(line)
           with open(dupfile, 'ab') as new_file:
                new_file.write(line)
        else:
            blf.add(line)
    print "lines:",lines_len," => ","nlines:",len(blf)
    with open(blofile, 'wb') as blfile:
        pickle.dump(blf, blfile)
    with open(ofile, 'wb') as outfile:
        outfile.writelines(lines)

@log_deco(False)
def filter_bigfile2(ifile,ofile):
    import contextlib,mmap
    with open(ifile, 'r') as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
            lines = f.readlines()
            print len(lines)
            with open(ofile, 'wb') as new_file:
                new_file.writelines(list(set(lines)))

@profile
def test():
    with open(r"D:\DB\txt2\search\1_2.txt",'r') as f:
        txt=f.read()

def test_source():
    import pstats
    p=pstats.Stats(r"d:\temp\test.txt")
    p.sort_stats("time").print_stats(20)


if __name__ == '__main__':
    ifile=r"D:\DB\Splited\1_1.txt"
    ifile=r"D:\DB\txt\库1.txt".decode('utf-8')
    ofile=r"d:\temp\test.txt"
    idir = r"D:\DB\txt2"
    odir = r"D:\DB\txt2\smallsize"
    #dir_dirs(r"D:\DB\txt2",ofile)
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
    #test()
    #python -m cProfile ./wuyun/txthelper.py -o result
    #python -m memory_profiler ./wuyun/txthelper.py
    #filter_bigfile(r'D:\DB\Splited\天涯论坛4000w数据(1).txt'.decode('utf-8'),r'D:\DB\txt2\test.txt')
    '''
    while True:
    block = f.read(1024)
    if not block:
        break
    '''
    #bloom_filter(r'D:\DB\txt2\search\1_2.txt',r'D:\DB\txt2\test.txt',r'D:\DB\txt2\dup.txt',r"D:\DB\txt2\bloom\test.bloom",5800000)
    #exit(0)
