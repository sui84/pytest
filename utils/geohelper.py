#encoding=utf-8
import math
from geopy.geocoders import Nominatim
import imagehelper

class GeoHelper(object):
    def __init__(self):
        pass

    def ConvertGps(self,du,fen,miao):
        num = float(du) + float(fen)/60 + float(miao)/3600
        return num

    def ConvertGoogleToBaidu(self,wdu,jdu):
        #转换为百度标准
        x_pi = 3.14159265358979324 * 3000.0 / 180.0
        x = jdu
        y = wdu
        z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
        theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
        jdu = z * math.cos(theta) + 0.0065
        wdu = z * math.sin(theta) + 0.006
        wdu = str(wdu)
        jdu = str(jdu)
        return {"wdu":wdu,"jdu":jdu}

    def Getlocation(self,ti,la):
        # ti 纬度 la 经度
        #发送http请求获取具体位置信息-不准!
        '''
        url = 'http://api.map.baidu.com/geocoder/v2/'
        ak = 'ak=1aZ2PQG7OXlk9E41QPvB9WjEgq5WO8Do'
        #back='&callback=renderReverse&location='
        back='&location='
        #location='34.992654,108.589507'
        location='%d,%d' % (ti,la)
        output = '&output=json&pois=0'
        url = url + '?' + ak + back + location + output

        temp = urllib2.urlopen(url)
        hjson = json.loads(temp.read())
        locate = hjson["result"]["formatted_address"]
        print locate
        mapinfo = hjson["result"]["sematic_description"]
        '''
        geolocator = Nominatim()
        s="%f,%f" % (ti,la)
        print s
        location = geolocator.reverse(s)
        print(location.address)
        print((location.latitude, location.longitude))

if __name__ == '__main__':
    im=imagehelper.ImageHelper()
    pos = im.GetImageInfo(r"d:\temp\test2.jpg",3)
    print pos
    g = GeoHelper()
    g.Getlocation(pos.get("wdu"),pos.get("jdu"))

