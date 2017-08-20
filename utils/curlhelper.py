#encoding=utf-8
import pycurl

#创建一个同libcurl中的CURL处理器相对应的Curl对象
c = pycurl.Curl()

c.setopt(pycurl.URL, 'https://mm.taobao.com/json/request_top_list.htm?page=1')

# 设置证书
c.setopt(pycurl.CAINFO, r'E:\01_SOFT\Python27\crt\curl-ca-bundle.crt')

#执行上述访问网址的操作
c.perform()
