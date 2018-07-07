#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import os
import time
'''
移动小于180M文件到另一个目录 dir_fmove
删除空目录 dir_files -> delete_gap_dir
列出所有子目录下文件路径和大小 dir_files
利用正则搜索字符串 search_file
目录下两个两个地合并文件，适用于大些的文件 combine_file
合并同一个目录下的所有文件，适用于小文件 combine_dir
'''

MaxFileSize = 180*1024*1024
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

def dir_only_files(idir):
    # not return files in subdir
    fs = []
    files=os.listdir(idir)
    for file in files:
        f=os.path.join(idir,file)
        if os.path.isfile(f):
            fs.append(f)
    return fs


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

def mk_subfile(lines,head,srcName,sub):
    [des_filename, extname] = os.path.splitext(srcName)
    filename  = des_filename + '_' + str(sub) + extname
    print( 'make file: %s' %filename)
    fout = open(filename,'w')
    try:
        fout.writelines([head])
        fout.writelines(lines)
        return sub + 1
    finally:
        fout.close()

def splitfile_byline(filename,count):
    fin = open(filename,'r')
    try:
        head = fin.readline()
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mk_subfile(buf,head,filename,sub)
                buf = []
        if len(buf) != 0:
            sub = mk_subfile(buf,head,filename,sub)
    finally:
        fin.close()

if __name__ == '__main__':
    begin = time.time()
    #splitfile_byline(r'D:\DB\txt2\big\tianya.csv'.decode('utf-8'),2000000)
    combine_dir(r"D:\DB\passdict\wordlist",r"D:\DB\passdict")
    end = time.time()
    print('time is %d seconds ' % (end - begin))

