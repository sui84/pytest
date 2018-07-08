#!python
# -*- coding: utf-8 -*-
import win32gui
import win32ui
import win32con
import win32api
import os
import time
import traceback
'''
安装为服务时候报错
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
error: BitBlt failed
'''

DirPath=r"D:\DB\img"
LogFile=r"d:\temp\log.txt"

def screen_dump(ofile=os.path.join(DirPath,time.strftime('%Y%m%d%H%M%S')+'.bmp')):
    try:
        # 获取桌面
        hdesktop = win32gui.GetDesktopWindow()

        # 分辨率适应
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

        # 创建设备描述表
        desktop_dc = win32gui.GetWindowDC(hdesktop)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)

        # 创建一个内存设备描述表
        mem_dc = img_dc.CreateCompatibleDC()

        # 创建位图对象
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(img_dc, width, height)
        mem_dc.SelectObject(screenshot)

        # 截图至内存设备描述表
        mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

        # 将截图保存到文件中
        screenshot.SaveBitmapFile(mem_dc, ofile)

        # 内存释放
        mem_dc.DeleteDC()
        win32gui.DeleteObject(screenshot.GetHandle())
    except Exception,e:
        msg = "[%s]Error:%s\n%s" % (time.ctime(),e.message,traceback.format_exc())
        with open(LogFile,'a') as f:
            f.write(msg)

def screen_dump2(ofile=os.path.join(DirPath,time.strftime('%Y%m%d%H%M%S')+'.bmp')):
    # PIL简单实现截图，只能截图最上层窗口
    from PIL import Image,ImageGrab
    bbox = (1085, 102, 1368, 373)
    #img = ImageGrab.grab(bbox)
    img = ImageGrab.grab()
    img.save(ofile)
    img.show()

def screen_dump3(ofile=os.path.join(DirPath,time.strftime('%Y%m%d%H%M%S')+'.bmp')):
    import win32gui
    import win32ui
    import win32con
    from ctypes import windll
    from PIL import Image
    # 对后台应用程序截图，程序窗口可以被覆盖，但如果最小化后只能截取到标题栏、菜单栏等。
    # 获取要截取窗口的句柄
    hwnd = win32gui.FindWindow("Afx:01370000:8:00010003:00000000:00200757", None)

    # 获取句柄窗口的大小信息
    # 可以通过修改该位置实现自定义大小截图
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hwndDC = win32gui.GetWindowDC(hwnd)

    # 创建设备描述表
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)

    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()

    # 创建位图对象
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    # 截图至内存设备描述表
    img_dc = mfcDC
    mem_dc = saveDC
    mem_dc.BitBlt((0, 0), (w, h), img_dc, (100, 100), win32con.SRCCOPY)

    # 将截图保存到文件中
    saveBitMap.SaveBitmapFile(mem_dc, ofile)


    # 改变下行决定是否截图整个窗口，可以自己测试下
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    print(result)

    # 获取位图信息
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    # 生成图像
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    # 存储截图
    if result == 1:
        #PrintWindow Succeeded
        im.save("test.png")
        im.show()

if __name__=='__main__':
    '''
    screen_dump3()
    exit(0)
    screen_dump2(r"d:\temp\test.jpg")
    exit(0)
    '''
    fname=time.strftime('%Y%m%d%H%M%S')+'.bmp'
    ofile=os.path.join(DirPath,fname)
    screen_dump(ofile)
