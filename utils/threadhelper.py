#encoding=utf-8
import threadpool
import confhelper
import os
import threadpool
from threading import Thread

'''

'''
class ThreadHelper(object):
    def __init__(self):
        self.confile = r"..\conf\test.conf"
        self.theadnum = 10
        if os.path.exists(self.confile):
            conf = confhelper.ConfHelper(self.confile)
            thread = conf.GetConfig("thread","theadnum")
            if thread.isdigit():
                self.threadnum =int(thread)

    #用多线程下载
    def WorkWithMultipleThreads(self,func,data):
        pool = threadpool.ThreadPool(self.theadnum)
        reqs = threadpool.makeRequests(func, data)
        [pool.putRequest(req) for req in reqs]
        pool.wait()
