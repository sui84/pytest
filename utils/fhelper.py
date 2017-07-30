#encoding=utf-8
import json
import tablib
from pymongo import MongoClient
'''
r 只读
w
a 追加
r+b 读写,b是二进制读写
w+b 写读
a+b 追加及读
w+ 打开文件会将原文件内容删除，可以同时对文件进行读写
r+ 打开文件会保持原文件内容不变，同样可以同时对文件进行读写
'''
class FHelper(object):
    def __init__(self, filename=r'd:\temp\test.txt'):
        self.fname = filename

    def GetAllLines(self):
        f = file(self.fname,'rb')
        return f.readlines()
    def SaveLine(self,line):
        f = file(self.fname,'w') #直接清空，不能用f.readline()
        f.write(line)
        #f.flush() #立刻写进去
        f.close() #写进IO
    def SaveDict(self,dictObj):
        jsObj = json.dumps(dictObj)
        fileObject = open(self.fname, 'w')
        fileObject.write(jsObj)
        fileObject.close()
    def SaveDictList(self,dictListObj):
        fileObject = open(self.fname, 'w')
        for dictObj in dictListObj:
            jsObj = json.dumps(dictObj)
            fileObject.write(jsObj)
            fileObject.write('\n')
        fileObject.close()
    def SaveContent(self,contents):
        fileObject = open(self.fname, 'w')
        fileObject.write(contents)
        fileObject.close()
    def SaveDictListToType(self,dictListObj,type):
        types = ('json', 'xls', 'yaml', 'csv', 'dbf', 'tsv', 'html', 'latex', 'xlsx', 'ods')
        validType = False
        typeIndex = 0
        for i in range(0, len(types)):
            if types[i].upper()==type.upper():
                validType = True
                typeIndex =i
                break
        if validType:
            data=[]
            fileObject = open(self.fname, 'w')
            if len(dictListObj)>1:
                headers=tuple(dictListObj[0])
                for dictObj in dictListObj:
                    data.append(tuple(dictObj.values()))
                data=tablib.Dataset(*data,heaaders=None)
                if types[typeIndex].upper()=='json'.upper():
                    fileObject.write(data.json)
                if types[typeIndex].upper()=='xls'.upper():
                    fileObject.write(data.json)
                if types[typeIndex].upper()=='yaml'.upper():
                    fileObject.write(data.json)
                if types[typeIndex].upper()=='csv'.upper():
                    fileObject.write(data.json)
                if types[typeIndex].upper()=='dbf'.upper():
                    fileObject.write(data.json)
                if types[typeIndex].upper()=='tsv'.upper():
                    fileObject.write(data.json)
                if types[typeIndex].upper()=='html'.upper():
                    fileObject.write(data.json)
                if types[typeIndex].upper()=='latex'.upper():
                    fileObject.write(data.json)
                if types[typeIndex].upper()=='xlsx'.upper():
                    fileObject.write(data.json)
                if types[typeIndex].upper()=='ods'.upper():
                    fileObject.write(data.json)
                fileObject.close()

