#encoding=utf-8
import threadpool
import confhelper
import os
import threadpool
from threading import Thread
import timehelper
import traceback
import itertools

'''

'''
class ThreadHelper(object):
    def __init__(self):
        self.confile = r"..\conf\test.conf"
        self.threadnum = 10
        if os.path.exists(self.confile):
            conf = confhelper.ConfHelper(self.confile)
            thread = conf.GetConfig("others","threadnum")
            if thread<>None and thread.isdigit():
                self.threadnum =int(thread)

    #多线程
    def WorkWithMultipleThreads(self,func,data):
        pool = threadpool.ThreadPool(self.threadnum)
        reqs = threadpool.makeRequests(func, data)
        [pool.putRequest(req) for req in reqs]
        pool.wait()


    #多进程
    #@timehelper.elapsedtimedeco(True)
    def MultiExecute(self,func,args):
        try:
            print self.threadnum
            from multiprocessing import Pool
            pool = Pool(processes = self.threadnum)
            #PicklingError: Can't pickle <type 'instancemethod'>: attribute lookup __builtin__.instancemethod failed
            pool.map(func,args)
            #pool.apply_async(func,args)
            #pool.map(func, itertools.izip(arg1, itertools.repeat(arg2)))
            pool.close()
            pool.join()
        except Exception,e:
            print  'Error:',e.message,'\n',traceback.format_exc()

    #多线程
     #@timehelper.elapsedtimedeco(True)
    def MultiThreadExecute(self,func,args):
        try:
            print self.threadnum
            from multiprocessing.dummy import Pool
            pool = Pool(processes = self.threadnum)
            pool.map(func,args)
            pool.close()
            pool.join()
        except Exception,e:
            print  'Error:',e.message,'\n',traceback.format_exc()

    #协程
    def MultiGEventExecute(self,func,args):
         from gevent.pool import Pool
         pool = Pool(self.threadnum)
         return pool.map(func,args)
