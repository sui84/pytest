#encoding=utf-8
import string
import pickle
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



