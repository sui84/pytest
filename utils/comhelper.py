import win32com.client
import win32api
import win32con

def excel_app():
    o = win32com.client.Dispatch("Excel.Application")
    o.Visible = 1
    o.Workbooks.Add() # for office 97 – 95 a bit different!
    o.Cells(1,1).Value = "Hello"

def word_app():
    w=win32com.client.Dispatch("Word.Application")
    w.Visible=1
    w.WindowState = win32com.client.constants.wdWindowStateMinimize

def msg_box():
    win32api.MessageBox(win32con.NULL, 'Python 你好！', '你好', win32con.MB_OK)

def reg():
    keyname='Software\Microsoft\Internet Explorer\Main'
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, keyname, 0, win32con.KEY_ALL_ACCESS)
    print win32api.RegQueryValueEx(key,'Start Page')
    page = 'www.linuxidc.net'
    title = 'I love sina web site!'
    search_page = 'http://www.linuxidc.com'
    win32api.RegSetValueEx(key, 'Start Page', 0, win32con.REG_SZ, page)
    win32api.RegSetValueEx(key, 'Window Title', 0, win32con.REG_SZ, title)
    win32api.RegSetValueEx(key, 'Search Page', 0, win32con.REG_SZ, search_page)
