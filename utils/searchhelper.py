#encoding=utf-8
import threadhelper
import commonhelper
#from multiprocessing.dummy import Pool
from multiprocessing import Pool
from itertools import product
import timehelper
import traceback
import fhelper
import pandas as pd
import strhelper
import sys
import os
sys.setdefaultencoding('utf-8')
'''
从目录DIR_PATH所有文件中查找STR_FILE里的字符串，结果存入OUT_FILE
'''


DIR_PATH = r"D:\DB\txt"
OUT_FILE = r"d:\temp\result.txt"
STR_FILE = r"D:\Temp\FindString2.txt"
PNUM = 10

def WrapperSearchInFile(args):
    #多个参数用这层包起来
    return SearchFile(*args)

def SearchFile(fname,strs):
    try:
        print fname
        content=open(fname,'rb').read()
        for str in strs:
            if str in content:
                print "found ",str
                lines = open(fname,'rb').readlines()
                for line in lines:
                    if str in line:
                        with open(OUT_FILE,'ab') as f:
                            f.write("[%s]:" % (str) )
                            f.writelines(line)
    except Exception,e:
        print 'Error:',e.message,'\n',traceback.format_exc()


@timehelper.elapsedtimedeco(True)
def MultiProcess(strs=None):
    pool = Pool(PNUM)
    files = commonhelper.GetDirFiles(DIR_PATH)
    args=[]
    if strs==None:
        strs = fhelper.FHelper(STR_FILE).GetAllLinesWithoutEnter()
    for file in files:
        args.append((file,strs))
    pool.map(WrapperSearchInFile,args)

def DropDuplicateLine(ipath):
    str=r'd:\DB\txt'
    rstr = r'd:\DB\txt2'
    #用正则替换字符串会带来字符编码问题
    #opath = strhelper.StrHelper().ReplaceIgnorecase(ipath,str,rstr)
    #opath = strhelper.StrHelper().ConvertToUnicode(opath)
    opath = ipath.replace(r'D:\DB\txt',r'D:\DB\txt2')
    print ipath,'->',opath
    lines = fhelper.FHelper(ipath).GetAllLinesWithoutEnter()
    df=pd.DataFrame({"line":lines})
    result = df.drop_duplicates()
    nlines = result.line.tolist()
    #f = fhelper.FHelper(opath)
    #f.SaveLines(nlines)
    newlines = '\n'.join(nlines)
    dirname=os.path.dirname(opath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(opath,'w') as f:
        f.writelines(newlines)

@timehelper.elapsedtimedeco(True)
def MultiProcessDropDuplicateLine():
    pool = Pool(PNUM)
    files = commonhelper.GetDirFiles(DIR_PATH)
    pool.map(DropDuplicateLine,files)


if __name__ == '__main__':
    #strs=["dd","sssss"]
    #MultiProcess(strs)

    #MultiProcess()
    #fhelper.FHelper(OUT_FILE).DeleteDuplicateLine()

    #elapsed time: 2661980.999947 ms
    MultiProcessDropDuplicateLine()



