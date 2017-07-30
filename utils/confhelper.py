#encoding=utf-8
import ConfigParser
import string

class ConfHelper(object):
    def __init__(self, filename=r'd:\temp\test.conf'):
        self.fname = filename
        self.config=ConfigParser.ConfigParser()
        self.config.read(self.fname)

    def GetAllConfig(self):
        print self.config.sections()
        for section in self.config.sections():
            print section
            for option in self.config.options(section):
                print " ",option,"=",self.config.get(section,option)
    def GetSectionConfig(self,section):
        for option in self.config.options(section):
              print " ",option,"=",self.config.get(section,option)
        return self.config.options(section)
    def GetConfig(self,section,option):
        return self.config.get(section,option)
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

