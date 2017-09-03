#encoding=utf-8
import string
import pickle
import json
#S.split(str,'')
#S.join(list,'')
class StrHelper(object):
    def __init__(self):
        print 'test'

    def SerializeString(self,obj):
        dumpsed = pickle.dumps(obj)
        return dumpsed

    def SerializeToFile(self,obj,ofile):
        dumpsed = pickle.dumps(obj)
        pickle.dump(obj,open(ofile,'w'))

    def Deserialize(self,dumpsed):
        loadsed = pickle.loads(dumpsed)
        return loadsed

    def DeserializeFromFile(self,ifile):
        loadsed = pickle.load(open(ifile,'r'))
        return loadsed

    def Jsonstr2Obj(self,jsonstr):
        obj =json.loads(jsonstr)
        return obj

    def Obj2JsonStr(self,obj):
        jsonstr =json.dumps(obj)
        return jsonstr



