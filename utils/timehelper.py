#encoding=utf-8
import time
'''
time.time()
time.localtime()
time.gmtime()
time.mktime(time.localtime())
'''


class TimeHelper(object):
    def __init__(self):
        print 'test'

    def GetCurrentTimeStr(self, fmt='%Y/%m/%d %H:%M:%S'):
        return time.strftime(fmt)


