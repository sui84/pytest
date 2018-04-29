#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import datetime
import Bazi
from utils.db import sqlhelper
from utils import setting
import traceback
mysqldb = setting.YAMLDATA.get('mysqldb2')
host,user,pwd,db=mysqldb.get('host'),mysqldb.get('user'),mysqldb.get('pwd'),mysqldb.get('bazidb')
sh=sqlhelper.SqlHelper(host,user,pwd,db,'mysql')



def save_paipan(selsql='select id,sex,year,month,day,hour,minute from mingzhu '
           ,updsql="update mingzhu set lunar='%s',lyear=%d,lmonth=%d,lday=%d,leap=%d,ygan='%s',yzhi='%s',mgan='%s',mzhi='%s',dgan='%s',dzhi='%s',hgan='%s',hzhi='%s',bjq='%s',bjqdt='%s',fjq='%s',fjqdt='%s',note='%s',ygindex=%d,yzindex=%d,mgindex=%d,mzindex=%d,dgindex=%d,dzindex=%d,hgindex=%d,hzindex=%d where id=%d"
           ,updysql="delete from dayun where pid=%d ; insert into dayun(pid,dtyear,dtmonth,dtday,dthour,spanyear,spanmonth,spanday,spanhour,year1,gan1,zhi1,year2,gan2,zhi2,year3,gan3,zhi3,year4,gan4,zhi4,year5,gan5,zhi5,year6,gan6,zhi6,year7,gan7,zhi7,year8,gan8,zhi8) \
values(%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,'%s','%s',%d,'%s','%s',%d,'%s','%s',%d,'%s','%s',%d,'%s','%s',%d,'%s','%s',%d,'%s','%s',%d,'%s','%s')"):
    results=sh.ExecQuery(selsql)
    for result in results:
        try:
            id,sex,year,month,day,hour,minute=result[0],result[1],result[2],result[3],result[4],result[5],result[6]
            dt=datetime.datetime(year,month,day,hour,minute)
            sexflag = 1
            if sex=='男':
                sexflag = 0
            bz=Bazi.bazi(dt,sexflag)
            bz.Paipan()
            lunar = bz.print_lunar().decode('utf-8')
            lyear,lmonth,lday,leap = bz.Solar2Lunar(dt)
            ygan,yzhi,mgan,mzhi,dgan,dzhi,hgan,hzhi = bz.Tiangan[bz.bazi[0]],bz.Dizhi[bz.bazi[1]],bz.Tiangan[bz.bazi[2]],bz.Dizhi[bz.bazi[3]]\
                                                     ,bz.Tiangan[bz.bazi[4]],bz.Dizhi[bz.bazi[5]],bz.Tiangan[bz.bazi[6]],bz.Dizhi[bz.bazi[7]]
            bjq,bjqdt,fjq,fjqdt=bz.Jieqi[bz.bazi[3]],bz.bjq,bz.Jieqi[bz.bazi[3]+1],bz.fjq
            note = bz.print_bazi().decode('utf-8')
            ygindex,yzindex,mgindex,mzindex,dgindex,dzindex,hgindex,hzindex = bz.bazi[0],bz.bazi[1],bz.bazi[2],bz.bazi[3],bz.bazi[4],bz.bazi[5],bz.bazi[6],bz.bazi[7]
            sql = updsql % (lunar,lyear,lmonth,lday,leap,ygan,yzhi,mgan,mzhi,dgan,dzhi,hgan,hzhi,bjq,bjqdt,fjq,fjqdt,note,ygindex,yzindex,mgindex,mzindex,dgindex,dzindex,hgindex,hzindex,id)
            sh.ExecNonQuery(sql)
            dtyear,dtmonth,dtday,dthour =  bz.jydt.year,bz.jydt.month,bz.jydt.day,bz.jydt.hour
            spanyear,spanmonth,spanday,spanhour = bz.qyspan
            year1,gan1,zhi1,year2,gan2,zhi2,year3,gan3,zhi3,year4,gan4,zhi4,year5,gan5,zhi5,year6,gan6,zhi6,year7,gan7,zhi7,year8,gan8,zhi8=bz.GetDayun()
            sql = updysql % (id,id,dtyear,dtmonth,dtday,dthour,spanyear,spanmonth,spanday,spanhour,year1,gan1,zhi1,year2,gan2,zhi2,year3,gan3,zhi3
                             ,year4,gan4,zhi4,year5,gan5,zhi5,year6,gan6,zhi6,year7,gan7,zhi7,year8,gan8,zhi8)
            sh.ExecNonQuery(sql)

        except Exception,e:
            print 'error:',e.message,traceback.format_exc()

if __name__ == '__main__':
    save_paipan()
