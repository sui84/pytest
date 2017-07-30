#encoding=utf-8
import json
from pymongo import MongoClient

class FHelper(object):
    def __init__(self, filename=r'd:\temp\test.html'):
        self.fname = filename

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
