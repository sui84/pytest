#encoding=utf-8
import json
from pymongo import MongoClient

class MgHelper(object):
    """ 并保存到MongoDB """
    def __init__(self, server='localhost',port=27017,dbname='Collections',tbname='jsontxt'):
        self.server = server
        self.port = port
        self.dbname = dbname
        self.tbname= tbname
        self.mongo = MongoClient(self.server , self.port)
        self.db = self.mongo[self.dbname]

    def SaveFile(self,fname,tbname='jsontxt'):
        f = file(fname)
        j = json.loads(f.read())
        table=self.db[tbname]#表名
        id = table.save(j)
        return id
    def SaveDictObjs(self,dictListObj,tbname='jsontxt'):
        table=self.db[tbname]#表名
        for dictObj in dictListObj:
        # jsObj = json.dumps(dictObj)
            id = table.insert(dictObj)
        return id
