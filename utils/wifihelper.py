# coding:utf-8
import time  #时间
import pywifi  #破解wifi
from pywifi import const  #引用一些定义

wifi = pywifi.PyWiFi()

def test_connect(ssid,findStr):#测试链接
        iface = wifi.interfaces()[0]#抓取第一个无限网卡
        iface.disconnect() #测试链接断开所有链接
        time.sleep(1) #休眠1秒

        #测试网卡是否属于断开状态，
        assert iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
        profile = pywifi.Profile()  #创建wifi链接文件
        profile.ssid = ssid #wifi名称
        profile.auth = const.AUTH_ALG_OPEN  #网卡的开放，
        profile.akm.append(const.AKM_TYPE_WPA2PSK)#wifi加密算法
        profile.cipher = const.CIPHER_TYPE_CCMP    #加密单元
        profile.key = findStr #密码

        iface.remove_all_network_profiles() #删除所有的wifi文件
        tmp_profile = iface.add_network_profile(profile)#设定新的链接文件
        iface.connect(tmp_profile)#链接
        time.sleep(5)
        print iface.status()
        if iface.status() == const.IFACE_CONNECTED:  #判断是否连接上
            isOK=True
        else:
            isOK=False
        #iface.disconnect() #断开
        #time.sleep(1)
        #检查断开状态
        #assert iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
        print isOK

if __name__ == "__main__":
        test_connect('ttt','ttt@2')


