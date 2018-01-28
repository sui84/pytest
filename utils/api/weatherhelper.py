#encoding=utf-8
import requests
import json
import math
from pyquery import PyQuery as pq

class WeatherHelper(object):
    def __init__(self):
        self.weather="http://d3.weather.com.cn/webgis_rain_new/webgis/ele?lat=%s&lon=%s&callback=fc5m&_=1470809429568"
        # $('.con_tab-tab').text()
        self.zhuhaiyj="http://www.zhmb.gov.cn:8000/jeecms/web/yjfw/fqyj"
        self.zhuhaiti1="http://www.zhmb.gov.cn:8000/jeecms/web/index"
        self.zhuhaiti="http://www.zhpmsc.org.cn/WeChat/monitorController/dqtqs"
        # $('.div01').text()  $('.div02').text()  $('.cont_top03 p').text()
        self.zhuhaiti2= "http://www.zhpmsc.org.cn/WeChat/monitorController/index"

    def GetZhuhaiYJ(self):
        d=pq(url=self.zhuhaiyj)
        msg = d('.con_tab-tab').text()
        d=pq(url=self.zhuhaiti2)
        msg += d('.div01').text()+d('.div02').text() + d('.cont_top03 p').text()
        return msg

    def GetWeather(self,wdu,jdu,location):
        '''在读取经纬度时涉及到一个问题，由于百度地图与谷歌地图采用的是不同协议的坐标，腾讯、高德地图与谷歌地图采用的是同种协议。
        而微信的经纬度信息是腾讯地图给出的，在网站上查看中国天气网发送的url请求可知，中国天气网采用的是百度地图，因此在查询之前需要对经纬度信息做一次转换。
        转换为百度标准'''
        x_pi = 3.14159265358979324 * 3000.0 / 180.0
        x = jdu
        y = wdu
        z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
        theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
        jdu = z * math.cos(theta) + 0.0065
        wdu = z * math.sin(theta) + 0.006
        wdu = str(wdu)
        jdu = str(jdu)
        Lmesag = u"您的位置："
        Lmesag += location
        url = self.weather % (wdu,jdu)
        print url
        myres = requests.get(url)
        if myres.status_code != 200:
         if myres.status_code == 500:
             return u"服务器未响应，请稍后再试~"+myres.status_code
        myres.encoding = 'utf-8'
        text = myres.text
        text = text[9:-2]
        data = json.loads(text)
        pretime = data['time']
        msg = data['msg']
        pretime1 = u"查询时间："
        pretime1 += pretime
        msg1 = "天气预报：\n中国天气网雷达数据(雷达外推数据，仅供参考)："
        msg1 += msg
        Lmesag += '\n'
        Lmesag += pretime1
        Lmesag += '\n'
        Lmesag += msg1
        cyres = requests.get('http://www.caiyunapp.com/fcgi-bin/v1/api.py?lonlat=' + jdu + ',' + wdu + '&format=json&product=minutes_prec&token=96Ly7wgKGq6FhllM&random=0.8600497214532319')
        cyres.encoding = "utf-8"
        cyData = json.loads(cyres.text)
        cymsg = u"\n\n彩云天气数据(准确率较高):"
        #cymsg += cyData['summary']
        cytemp = u"\n温度："
        cytemp += str(cyData['temp'])
        cymsg += cytemp
        cymsg +=u"\n未来1小时天气预报："
        cymsg += cyData['summary']
        Lmesag += cymsg
        return Lmesag
