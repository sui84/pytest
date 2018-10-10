#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import win32serviceutil
import win32service
import win32event
import os
import ServiceManager
import sys
import winerror
import loghelper
import SimpleHTTPServer
import SocketServer
'''
#1.安装服务
python PythonService.py install
#2.让服务自动启动
python PythonService.py --startup auto install
#3.启动服务
python PythonService.py start
#4.重启服务
python PythonService.py restart
#5.停止服务
python PythonService.py stop
#6.删除/卸载服务
python PythonService.py remove
'''


LogFile = r"d:\temp\test.txt"
Interval = 5 * 60


class PythonService(win32serviceutil.ServiceFramework):

    _svc_name_ = "PythonService"  #服务名
    _svc_display_name_ = "Python Service Test"  #服务在windows系统中显示的名称
    _svc_description_ = "This is a python service test code "  #服务的描述

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = loghelper.create_logger( LogFile)
        self.run = True


    def SvcDoRun(self):
        self.logger.info("service is run....")
        #Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        #httpd = SocketServer.TCPServer(("", 8001), Handler)
        import webhelper
        import thread
        thread.start_new(webhelper.test_app, ())
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        #keyloghelper.key_log()
        #while self.run:
            #self.logger.info("I am runing....")
            #screenhelper.screen_dump()
            #screenhelper.screen_dump2()
            #keyloghelper.key_log()
            #time.sleep(Interval)


    def SvcStop(self):
        self.logger.info("service is stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False

if __name__=='__main__':
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(ServiceManager.__file__)
            ServiceManager.PrepareToHostSingle(PythonService)
            ServiceManager.Initialize('PythonService', evtsrc_dll)
            ServiceManager.StartServiceCtrlDispatcher()
        except win32service.error, details:
            if details[0] == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(PythonService)
