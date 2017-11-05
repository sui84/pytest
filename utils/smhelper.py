#encoding=utf-8
import xlshelper
import lunarhelper
import datetime

ROWSTART = 2
ROWEND = 16
COLSTART = 1
COLEND = 11
RESULTCOLSTART = 13
RESULTCOLEND = 22
XLSFN = r'..\xlsx\sm.xlsx'

class SMHelper(object):
    def __init__(self):
        self.xh=xlshelper.XlsHelper(filename= XLSFN)
        self.ws = self.xh.GetWorkSheet(0)
        self.mingzhus= self.xh.GetRows(self.ws,ROWSTART,ROWEND,COLSTART,COLEND)

    def GetShun(self,sex,NG):
        if (sex==u'男' and NG%2==0) or (sex==u'女' and NG%2==1):
            shun=True
        elif (sex==u'男' and NG%2==1) or (sex==u'女' and NG%2==0):
            shun=False
        return shun

    def GetQiYun(self,sex,NG,birthdate,jqstart,jqend):
        shun = self.GetShun(sex,NG)
        if shun:
            years = abs(jqend-birthdate).days/3
            yu = abs(jqend-birthdate).days%3
        else:
            years = abs(birthdate-jqstart).days/3
            yu = abs(birthdate-jqstart).days%3
        months = yu * 4
        qiyundt = birthdate+datetime.timedelta(years= days=days,hours=hours,minutes=mins)
        datetime.datedelta


    def GetLunar(self):
        results=[]
        for id,name,sex,year,month,day,hour,min,yun,lunar in self.mingzhus:
            ct = datetime.datetime(year,month,day,hour,min,0)
            ln = lunarhelper.Lunar(ct)
            print(u'{} 姓名: {} 性别: {} 公历: {} 农历: {}'.format(id,name,sex,ln.localtime,ln.ln_date_str()))
            print(u'{} {}年 {}月 {}日 {}时'.format( ln.sx_year(), ln.gz_year(),ln.gz_month(), ln.gz_day(), ln.gz_hour()))
            jieqiid,zhiid,jieqi,jqstart,jqend=ln._get_jieqi()
            print(u'节气：{} 从 {} 到 {} '.format(jieqi,jqstart,jqend))
            NG,NZ = self.gzid_year()

            #print(u'岁数：{} 起运年：{} 起运岁数：{}'.format(ln.localtime.year))
            result = [ln.localtime,ln.ln_date_str(),jieqi,ln.sx_year(), ln.gz_year(),ln.gz_month(), ln.gz_day(), ln.gz_hour()]
            results.append(result)
        print len(self.mingzhus),len(results)
        self.xh.WriteRows(self.ws,results,ROWSTART,ROWEND,RESULTCOLSTART,RESULTCOLEND)


if __name__ == '__main__':
    sm = SMHelper()
    sm.GetLunar()
