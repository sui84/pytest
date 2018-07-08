#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import win32serviceutil
import win32service
import win32event
import thread

def log(message):
        logger = file("e:\log.txt","a")
        logger.write(message+"\r\n")
        logger.close()


class WindowsService(win32serviceutil.ServiceFramework):
        #这两行必须
        _svc_name_ = "WindowsService"
        _svc_display_name_ = "WindowsService"

        def __init__(self, args):
                win32serviceutil.ServiceFramework.__init__(self, args)
                self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

        def SvcStop(self):
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                win32event.SetEvent(self.hWaitStop)

        def SvcDoRun(self):
                import WebServer
                thread.start_new(WebServer.main, ())
                win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(WindowsService)
