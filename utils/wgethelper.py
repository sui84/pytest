import wget
import os
from multiprocessing import Pool
import timehelper
'''


'''

urls=['https://sourceforge.net/projects/ophcrack/files/tables/XP%20special/table2.index/download','https://sourceforge.net/projects/ophcrack/files/tables/XP%20special/table2.bin/download','https://sourceforge.net/projects/ophcrack/files/tables/XP%20special/table1.start/download','https://sourceforge.net/projects/ophcrack/files/tables/XP%20special/table1.index/download','https://sourceforge.net/projects/ophcrack/files/tables/XP%20special/table1.bin/download','https://sourceforge.net/projects/ophcrack/files/tables/XP%20special/table0.start/download','https://sourceforge.net/projects/ophcrack/files/tables/XP%20special/table0.index/download','https://sourceforge.net/projects/ophcrack/files/tables/XP%20special/table0.bin/download']

outs=['table2.index','table2.bin','table1.start','table1.index','table1.bin','table0.start','table0.index','table0.bin']
dir=r"D:\DB\rainbow\XP special"
dir2 = r"D:\DB\rainbow\Vista special"

args2=[('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/md5sum.txt/download','md5sum.txt')
	,('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/table3.start/download','table3.start')
	,('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/table3.index/download','table3.index')
	,('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/table3.bin/download','table3.bin')
	,('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/table2.start/download','table2.start')
	,('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/table2.index/download','table2.index')
	,('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/table2.bin/download','table2.bin')
	,('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/table1.start/download','table1.start')
	,('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/table1.index/download','table1.index')
	,('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/table1.bin/download','table1.bin')
	,('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/table0.start/download','table0.start')
	,('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/table0.index/download','table0.index')
	,('https://sourceforge.net/projects/ophcrack/files/tables/Vista%20special/table0.bin/download','table0.bin')]



@timehelper.elapsedtimedeco(True)
def MultiProcoess(strs=None):
    pool = Pool(10)
    '''
    args=[]
    i=0
    for url in urls:
        args.append((url,outs[i]))
        i+=1
    print len(urls)
    '''
    pool.map(MultiDownLoad,args2)


def MultiDownLoad(args):
	url,fname = args
	wget.download(url,os.path.join(dir2,fname)) 

if __name__ == '__main__': 
	MultiProcoess()