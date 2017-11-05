#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
from db import mghelper
import mathhelper
import multiprocessing
import urlparse
from py_linq import Enumerable
import pprint
import timehelper
import traceback
import webxmlhelper
import timehelper
import strhelper
import random

'''
citycodes=webxmlhelper.YAMLDATA.get('citycodes')
airurl= webxmlhelper.YAMLDATA.get('airurl')
action='getDomesticAirlinesTime'
airreqpath= webxmlhelper.XMLPATH % (action, 'Req')
airsoapaction= urlparse.urljoin(webxmlhelper.WXNameSpace, action)
queue = multiprocessing.Queue()
'''
tbname = "statimes"
url = webxmlhelper.YAMLDATA.get('trainurl')
mh=mghelper.MgHelper(server=webxmlhelper.YAMLDATA.get('mongoserver'),port=webxmlhelper.YAMLDATA.get('mongoport'),dbname=webxmlhelper.YAMLDATA.get('mongodb'))
proxiesfile = r'..\..\out\proxies2.txt'
with open(proxiesfile,'r') as f:
    data = f.read()
lines=data.splitlines()
proxies=[]
for proxy in lines:
    proxies.append ( {
          "http": proxy,
          "https": proxy,
        })


def ValifyProxy():
    proxiesfile = r'..\..\out\proxies.txt'
    proxiesfile2 = r'..\..\out\proxies2.txt'
    with open(proxiesfile,'r') as f:
        data = f.read()
    lines=data.splitlines()
    for proxy in lines:
        proxies = {
              "http": proxy,
              "https": proxy,
            }
        try:
            url = 'http://ws.webxml.com.cn/WebServices/TrainTimeWebService.asmx'
            xmlstr = '''<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:web="http://WebXml.com.cn/">
       <soap:Header/>
       <soap:Body>
          <web:getStationAndTimeByStationName>
             <!--Optional:-->
             <web:StartStation>广州</web:StartStation>
             <!--Optional:-->
             <web:ArriveStation>湛江</web:ArriveStation>
             <!--Optional:-->
             <web:UserID></web:UserID>
          </web:getStationAndTimeByStationName>
       </soap:Body>
    </soap:Envelope>'''
            resxml = webxmlhelper.HTTPHELPER.PostXMLRequest(url,xmlstr,proxies)
            result = webxmlhelper.XMLHELPER.GetDictsByXStr(resxml)
            r = result.get('Envelope').get('Body').get('getStationAndTimeByStationNameResponse').get('getStationAndTimeByStationNameResult').get('diffgram').get('getStationAndTime').get('TimeTable')
            if type(r) is list:
                at = r[0]
            else:
                at = r
            traincode = at.get('TrainCode').get('value')
            if traincode <>'----' and traincode <> None:
                print 'success proxy',proxy
                with open(proxiesfile2,'ab') as f:
                    f.write(proxy+'\n')
        except:
            print "failed proxy"

def SendRequest(reqxml):
    try:
        print reqxml
        #resxml = webxmlhelper.HTTPHELPER.WebServiceResponse(airurl, airsoapaction, reqxml)
        resxml = webxmlhelper.HTTPHELPER.PostXMLRequest(url,reqxml,random.choice(proxies))
        result = webxmlhelper.XMLHELPER.GetDictsByXStr(resxml)
        if tbname == "airlines":
            r = result.get('Envelope').get('Body').get('getDomesticAirlinesTimeResponse').get('getDomesticAirlinesTimeResult').get('diffgram').get('Airlines').get('AirlinesTime')
        elif tbname == "statimes":
            r = result.get('Envelope').get('Body').get('getStationAndTimeByStationNameResponse').get('getStationAndTimeByStationNameResult').get('diffgram').get('getStationAndTime').get('TimeTable')
        print r
        if type(r) is list:
            for at in r:
                #putinqueue(queue,at)
                SaveDB(at)
        else:
            #putinqueue(queue,r)
            SaveDB(r)
    except Exception,e:
        print  'Error:',e.message,'\n',traceback.format_exc()
        errorfile = r'..\..\out\errorxml.txt'
        with open(errorfile,'ab') as f:
            f.write(reqxml+"|||")

def SaveDB(at):
    result = getresult(at)
    if result <> None:
        mh.SaveDictObj(result,tbname)

def putinqueue(queue,at):
    result = getresult(at)
    queue.put(result)

def getresult(at):
    if tbname == "airlines":
            if at.get('AirlineCode').get('value') <> None:
                result =  {'Week':at.get('Week').get('value'),'AirlineStop':at.get('AirlineStop').get('value'),'StartDrome':at.get('StartDrome').get('value')
                ,'ArriveTime':at.get('ArriveTime').get('value'),'Company':at.get('Company').get('value'),'AirlineCode':at.get('AirlineCode').get('value')
                ,'StartTime':at.get('StartTime').get('value'),'ArriveDrome':at.get('ArriveDrome').get('value'),'Mode':at.get('Mode').get('value')}
                return result
    elif tbname == "statimes":
            if at.get('TrainCode').get('value') <> None and at.get('TrainCode').get('value') <>'----':
                result =  {'TrainCode':at.get('TrainCode').get('value'),'FirstStation':at.get('FirstStation').get('value'),'LastStation':at.get('LastStation').get('value')
                   ,'StartStation':at.get('StartStation').get('value'),'StartTime':at.get('StartTime').get('value'),'ArriveStation':at.get('ArriveStation').get('value')
                   ,'ArriveTime':at.get('ArriveTime').get('value'),'KM':at.get('KM').get('value'),'UseDate':at.get('UseDate').get('value')}
                return result

@timehelper.elapsedtimedeco(True)
def GetData(type):
    global tbname
    global url
    tbname = type
    sh = strhelper.StrHelper()
    if type == "airlines":
        citycodes = webxmlhelper.TESTDB.get('citycodes')
        reqarr = [(lambda x: sh.Convert2UTF8(x.get('Abbreviation')))(x) for x in citycodes]
        url= webxmlhelper.YAMLDATA.get('airurl')
        action='getDomesticAirlinesTime'
    elif type == "statimes":
        stations = webxmlhelper.TESTDB.get('stations')
        reqarr = [(lambda x: sh.Convert2UTF8(x.get('station')))(x) for x in stations]
        url= webxmlhelper.YAMLDATA.get('trainurl')
        action ="getStationAndTimeByStationName"

    reqpath= webxmlhelper.XMLPATH % (action, 'Req')
    with  open(reqpath,'r') as f:
        xmldata = f.read()

    combines = mathhelper.GetPermu(reqarr)
    reqxmls = webxmlhelper.SHHELPER.ReplaceListsString(xmldata,combines)

    num = len(reqxmls)
    print "Process start ",len(reqxmls)


    from multiprocessing import Pool
    pool = Pool(processes = webxmlhelper.THREADNUM)
    for i in range(num):
        #pool.apply_async(SendRequest, args=(reqxmls[i],))
        pool.apply(SendRequest, args=(reqxmls[i],))

    pool.close()
    pool.join()
    print "Process end , save data start:"

    #results= webxmlhelper.QueueToList(queue)
    #webxmlhelper.XLSHELPER.SaveDictsToSheet("airlines", results)
    #joblib.dump(results,airlinespath)


if __name__ == '__main__':
    #GetData("airlines")
    GetData("statimes")
    #ValifyProxy()
