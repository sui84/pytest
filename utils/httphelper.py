#encoding=utf-8
import httplib
import fhelper
import confhelper
import commonhelper
import loghelper


logger = loghelper.create_logger()

class HttpHelper(object):
    def __init__(self):
        self.headers={'Accept':"*/*"
                    ,'Connection': "Keep-Alive"
                    ,'Accept-Language': "zh-CN,zh;q=0.8"
                    ,'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
                    ,'Content-Type':"text/html; charset=utf-8"}
    
    # send get request
    def GetResponse(self,host):
        conn=httplib.HTTPConnection(host,url)
        #header错误会导致得到的数据乱码
        conn.request('GET',url,'',self.headers)
        res=conn.getresponse()
        if res.status == 200:
            data=res.read()
        else:
            data="%d %s %s" % (res.status,res.reason,str(res.msg))
        conn.close()
        return data
    
    # send post request    
    def PostResponse(self,host,parasdict,url):
        params = urllib.urlencode(parasdict)
        conn=httplib.HTTPConnection(host)
        #header错误会导致得到的数据乱码
        conn.request('POST',url,params,self.headers)
        res=conn.getresponse()
        if res.status == 200:
            data=res.read()
        else:
            data="%d %s %s" % (res.status,res.reason,str(res.msg))
        conn.close()
        return data
    
    # send soap request
    def WebServiceResponse(self,host,url,soapaction,xml):
        webservice = httplib.HTTP(host)
        webservice.putrequest("POST", url)
        webservice.putheader("Host", host)
        webservice.putheader("SOAPAction", soapaction)
        webservice.putheader("User-Agent", "Python Post")
        webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        webservice.putheader("Content-length", "%d" % len(xml))
        webservice.endheaders()
        print host,url,soapaction,xml
        webservice.send(xml)
        statuscode, statusmessage, header = webservice.getreply()
        if statuscode == 200:
            data=webservice.getfile().read()
        else:
            data="%d %s %s" % (statuscode,statusmessage,str(header))   
        print data
        webservice.close()
        return data

    
    loghelper.exception(logger)        
    def CallWebService(self,host,url,soapaction,ixml,oxml):
        fh=fhelper.FHelper(ixml)
        xml = fh.GetFileContent()
        result=http.WebServiceResponse(host,url,soapaction,xml)
        print oxml
        with open(oxml, 'w') as f:
            f.write(result)


if __name__ == '__main__':
    http=HttpHelper()
    #result=http.GetResponse(host)
    conf=confhelper.ConfHelper()
    confs = conf.GetSectionConfig("soaphttp")
    host=confs["soaphost"]
    url=confs["soapurl"]
    reqs = conf.GetListobjConfig("soaphttp","reqxml")
    ns = confs["namespace"]
    outxmldir=confs["outxmldir"]
    for req in reqs:
        action = req["action"]
        reqpath = req["reqpath"]
        soapaction=commonhelper.GetFullUrl(ns,action)
        outfpath=commonhelper.GetDstPath(outxmldir,reqpath)
        http.CallWebService(host,url,soapaction,reqpath,outfpath)

