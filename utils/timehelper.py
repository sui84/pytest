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

def elapsedtimedeco(arg=True):
    if arg:
        def _deco(func):
            def wrapper(*args,**kwargs):
                startTime = time.time()
                func(*args,**kwargs)
                endTime = time.time()
                msecs = (endTime - startTime) * 1000
                print "->elapsed time: %f ms" % msecs
            return wrapper
    else:
        def _deco(func):
            return func
    return _deco

if __name__ == '__main__':
    # 装饰器使用
    @elapsedtimedeco(True)
    def addFunc(a,b,c):
        print 'start'
        time.sleep(0.9)
        print a+b+c
        print 'end'

    addFunc(5,6,8)
