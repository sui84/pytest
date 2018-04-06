#encoding=utf-8
import matplotlib.pyplot as plt
import urllib
import json

def bar():
    plt.bar(left = (0,1),height = (1,0.5),width = 0.35)

    plt.show()
def bar2():
    import plotly.plotly
    import plotly.graph_objs as go
    trace = go.Box(
        x=[1, 2, 3, 4, 5, 6, 7]
    )
    data = [trace]
    plotly.offline.plot(data)  # 离线方式使用：offline

def getlnglat(address):
     url = 'http://api.map.baidu.com/geocoder/v2/'
     output = 'json'
     ak = 'c7aBgFWD6cMDPOe4BSiG8HLNlvXNKvCW'
     uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
     temp = urllib.urlopen(uri)
     temp = json.loads(temp.read())
     return temp

if __name__ == '__main__':
    pass
