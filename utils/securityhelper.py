#encoding=utf-8
import hashlib


class ConfHelper(object):
    def __init__(self):
        self.hash = hashlib.mds()

    def GetEncryString(self,str):
        #    hash.digest()
        hash.update(str)
        return self.hash.hexdigest()


