#encoding=utf-8
import time
'''
'''


class ModuleHelper(object):
    def __init__(self):
        print 'test'

    def ExecuteFunction(self,usrsp,mod,func):
        if usrsp != '':
            userspace = __import__(usrsp+mod)
            module = getattr(userspace,mod)
        else:
            module = __import__(usrsp+mod)
        function = getattr(module,func)
        function()
