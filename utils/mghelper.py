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
    def GetDBNames(self):
        # ls=list(db.Blog.find({"QQ":"2273075635"}))
        #  tuple(ls[0])
        # (u'QQ', u'Comment', u'isTransfered', u'Like', u'Title', u'URL', u'Transfer', u'Blog_cont', u'Share', u'Source', u'PubTime', u'_id')
        dbnames=self.mongo.collection_names(include_system_collections=False)
        return dbnames
    def GetDictHeader(self,tbname='jsontxt',con={}):
        dictObj = self.db[tbname].find_one(con)
        header = tuple(dictObj)
        return header
    def GetDictObj(self,tbname='jsontxt',con={}):
        dictObj = self.db[tbname].find_one(con)
        return dictObj
    def GetDictObjs(self,tbname='jsontxt',con={}):
        dictObjs = list(self.db[tbname].find(con))
        return dictObjs
    def GetDictObjsCnt(self,tbname='jsontxt',con={}):
        dictObjs = self.db[tbname].find(con).count()
        return dictObjs
    def RemoveTable(self,tbname='jsontxt',con={}):
        self.db[tbname].remove(con)
        return True
    def InsertTable(self,tbname='jsontxt',dictObjs={}):
        self.db[tbname].insert(dictObjs)
        return True
