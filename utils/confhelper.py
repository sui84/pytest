#encoding=utf-8
import ConfigParser
import string
import ast

class ConfHelper(object):
    def __init__(self, filename=r'd:\temp\test.conf'):
        self.fname = filename
        self.config=ConfigParser.ConfigParser()
        self.config.read(self.fname)
        self.confs = self.GetAllConfig()

    def GetAllConfig(self):
        confs = {}
        for section in self.config.sections():
            for option in self.config.options(section):
                confs[option] = self.config.get(section,option)
        return confs
    def ShowAllConfig(self):
        print self.config.sections()
        confs = {}
        for section in self.config.sections():
            print section
            for option in self.config.options(section):
                confs[option] = self.config.get(section,option)
                print " ",option,"=",self.config.get(section,option)
        return confs
    def GetSectionConfig(self,section):
        confs={}
        for option in self.config.options(section):
              print " ",option,"=",self.config.get(section,option)
              confs[option] = self.config.get(section,option)
        return confs
    def GetConfig(self,section,option):
        return self.config.get(section,option)
        
    def StrToDictList(self,str):
        listobj = ast.literal_eval(str)
        return listobj
        
    def GetListobjConfig(self,section,option):
        str = self.config.get(section,option)
        listobj = self.StrToDictList(str)
        return listobj
        
    def UpdateConfig(self,section,option,optionvalue):
        if not(self.config.has_section(section)):
            self.config.add_section(section)
        self.config.set(section,option,optionvalue)
        self.config.write(open(self.fname,'r+'))
        return True
    def RemoveSectionConfig(self,section):
        self.config.remove_section(section)
        # write to file
        with open(self.fname,"w+") as f:
            self.config.write(f)
            f.closed()
    def RemoveConfig(self,section,option):
        self.config.remove_option(section,option)
        # write to file
        with open(self.fname,"w+") as f:
            self.config.write(f)
            f.closed()

if __name__ == '__main__':
    print 'main'
