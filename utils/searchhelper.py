#encoding=utf-8
import threadhelper
import commonhelper
#from multiprocessing.dummy import Pool
from multiprocessing import Pool
from itertools import product
import timehelper
import traceback
import fhelper

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

if __name__ == '__main__':
    #strs=["369938016","sui84@126.com"]
    #MultiProcess(strs)
    MultiProcess()
    fhelper.FHelper(OUT_FILE).DeleteDuplicateLine()



