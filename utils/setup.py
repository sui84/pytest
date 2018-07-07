#encoding=utf-8
from distutils.core import setup
import py2exe
import glob


# 控制台界面
setup(console=["webhelper.py","test.py"],
      data_files=[("conf",
                   ["../conf/test.conf"]),
                  ("fonts",
                   glob.glob("fonts\\*.fnt"))],
)

# 图形用户界面
#setup(windows=["myscript.py"])
from distutils.core import setup
import py2exe
options = {"py2exe":{"compressed": 1, #压缩
                     "optimize": 2,
                     "bundle_files": 1 #所有文件打包成一个exe文件
                     }}
#setup(console=["./win32/keyloghelper.py"])
setup(service=["WindowsService"])
'''
import win32serviceutil
import win32event
import win32service
import socket
import servicemanager
import logging
import os

# windows service

安装成功了却启动不起来
python setup.py install
Installing service HelloWorld-Service
Service installed
'''
'''
class HelloWorldSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "HelloWorld-Service"
    _svc_display_name_ = "HelloWorld Service"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.stop_event = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('Stopping service ...')
        self.stop_requested = True

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    @staticmethod
    def main():
        # 运行程序
        file_path = os.path.split(os.path.realpath(__file__))[0] + '\\webhelper.py'
        print file_path
        try:
            execfile(file_path)
        except:
            pass


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(HelloWorldSvc)
'''
