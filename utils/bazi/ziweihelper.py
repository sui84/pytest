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
import collections
mysqldb = setting.YAMLDATA.get('mysqldb2')
host,user,pwd,db=mysqldb.get('host'),mysqldb.get('user'),mysqldb.get('pwd'),mysqldb.get('bazidb')
sh=sqlhelper.SqlHelper(host,user,pwd,db,'mysql')

'''
王亭之 安星法
'''

Tiangan = (u"甲",u"乙",u"丙",u"丁",u"戊",u"己",u"庚",u"辛",u"壬",u"癸","")
Dizhi = (u"子",u"丑",u"寅",u"卯",u"辰",u"巳",u"午",u"未",u"申",u"酉",u"戌",u"亥")
GongWei = (u"命宫",u"兄弟宫",u"夫妻宫",u"子女宫",u"财帛宫",u"疾厄宫",u"迁移宫",u"交友宫",u"事业宫",u"田宅宫",u"福德宫",u"父母宫")
NaYin = {u'甲子':u'海中金',u'乙丑':u'海中金',u'甲午':u'沙中金',u'乙未':u'沙中金'
         ,u'丙寅':u'炉中火',u'丁卯':u'炉中火',u'丙申':u'山下火',u'丁酉':u'山下火'
         ,u'戊辰':u'大林木',u'己巳':u'大林木',u'戊戌':u'平地木',u'己亥':u'平地木'
         ,u'庚午':u'路旁土',u'辛未':u'路旁土',u'庚子':u'壁上土',u'辛丑':u'壁上土'
         ,u'壬申':u'剑锋金',u'癸酉':u'剑锋金',u'入寅':u'金箔金',u'癸卯':u'金箔金'
         ,u'甲戌':u'山头火',u'乙亥':u'山头火',u'甲辰':u'覆灯火',u'乙巳':u'覆灯火'
         ,u'丙子':u'涧下水',u'丁丑':u'涧下水',u'丙午':u'天河水',u'丁未':u'天河水'
         ,u'戊寅':u'城头土',u'己卯':u'城头土',u'戊申':u'大驿土',u'己酉':u'大驿土'
         ,u'庚辰':u'白蜡金',u'辛巳':u'白蜡金',u'庚戌':u'钗钏金',u'辛亥':u'钗钏金'
         ,u'壬午':u'杨柳木',u'癸未':u'杨柳木',u'壬子':u'桑柘木',u'癸丑':u'桑柘木'
         ,u'甲申':u'泉中水',u'乙酉':u'泉中水',u'甲寅':u'大溪水',u'乙卯':u'大溪水'
         ,u'丙戌':u'屋上土',u'丁亥':u'屋上土',u'丙辰':u'沙中土',u'丁巳':u'沙中土'
         ,u'戊子':u'霹雳火',u'己丑':u'霹雳火',u'戊午':u'天上火',u'己未':u'天上火'
         ,u'庚寅':u'松柏木',u'辛卯':u'松柏木',u'庚申':u'石榴木',u'辛酉':u'石榴木'
         ,u'壬辰':u'长流水',u'癸巳':u'长流水',u'壬戌':u'大海水',u'癸亥':u'大海水'}
WhJu = {u"火":u"火六局",u"土":u"土五局",u"水":u"水二局",u"木":u"木三局",u"金":u"金四局"}
WhJuIndex = {u"火":6,u"土":5,u"水":2,u"木":3,u"金":4}

CSXingYao = [u"长生",u"沐浴",u"冠带",u"临官",u"帝旺",u"衰",u"病",u"死",u"墓",u"绝",u"胎",u"养"]
TSXingYao = [u"太岁",u"晦气",u"丧门",u"贯索",u"官府",u"小耗",u"岁破",u"龙德",u"白虎",u"天德",u"吊客",u"病符"]
JQXingYao = [u"将星",u"攀鞍",u"岁驿",u"息神",u"华盖",u"劫煞",u"灾煞",u"天煞",u"指背",u"咸池",u"月煞",u"亡神"]
BSXingYao = [u"博士",u"力士",u"青龙",u"小耗",u"将军",u"奏书",u"飞廉",u"喜神",u"病符",u"大耗",u"伏兵",u"官府"]

ZWMX = [u"平",u"庙",u"庙",u"旺",u"陷",u"旺",u"庙",u"庙",u"旺",u"平",u"闲",u"旺"]
TJMX = [u"庙",u"陷",u"旺",u"旺",u"庙",u"平",u"庙",u"陷",u"平",u"旺",u"庙",u"平"]
TYMX = [u"陷",u"陷",u"旺",u"庙",u"旺",u"旺",u"庙",u"平",u"闲",u"闲",u"陷",u"陷"]
WuQMX = [u"旺",u"庙",u"闲",u"陷",u"庙",u"平",u"旺",u"庙",u"平",u"旺",u"庙",u"平"]
TTMX = [u"旺",u"陷",u"闲",u"庙",u"平",u"庙",u"陷",u"陷",u"旺",u"平",u"平",u"庙"]
LZMX = [u"平",u"旺",u"庙",u"闲",u"旺",u"陷",u"平",u"庙",u"庙",u"平",u"旺",u"陷"]
TFMX = [u"庙",u"庙",u"庙",u"平",u"庙",u"平",u"旺",u"庙",u"平",u"陷",u"庙",u"旺"]
TYiMX = [u"庙",u"庙",u"闲",u"陷",u"闲",u"陷",u"陷",u"平",u"平",u"旺",u"旺",u"庙"]
TLMX = [u"旺",u"庙",u"平",u"地",u"庙",u"陷",u"旺",u"庙",u"平",u"平",u"庙",u"陷"]
JMMX = [u"旺",u"旺",u"庙",u"庙",u"平",u"平",u"旺",u"陷",u"庙",u"庙",u"旺",u"旺"]
TXaMX = [u"庙",u"庙",u"庙",u"陷",u"旺",u"平",u"旺",u"闲",u"庙",u"陷",u"闲",u"平"]
TLiMX = [u"庙",u"旺",u"庙",u"庙",u"旺",u"陷",u"庙",u"旺",u"陷",u"地",u"旺",u"陷"]
QSMX = [u"旺",u"庙",u"庙",u"陷",u"旺",u"平",u"旺",u"旺",u"庙",u"闲",u"庙",u"平"]
PJMX = [u"庙",u"旺",u"陷",u"旺",u"旺",u"闲",u"庙",u"庙",u"陷",u"陷",u"旺",u"平"]
ZhengYaoMX = [ZWMX,TFMX,TJMX,TYMX,WuQMX,TTMX,LZMX,TYiMX,TLMX,JMMX,TXaMX,TLiMX,QSMX,PJMX]

TKMX = [u"旺",u"旺",u"",u"庙",u"",u"",u"庙",u"",u"",u"",u"",u"旺"]
TYueMX = [u"",u"",u"旺",u"",u"",u"旺",u"",u"旺",u"庙",u"庙",u"",u""]
ZFMX = [u"旺",u"庙",u"庙",u"陷",u"庙",u"平",u"旺",u"庙",u"平",u"陷",u"庙",u"闲"]
YBMX = [u"庙",u"庙",u"旺",u"陷",u"庙",u"平",u"旺",u"庙",u"闲",u"陷",u"庙",u"平"]
WCMX = [u"旺",u"庙",u"陷",u"平",u"旺",u"庙",u"陷",u"平",u"旺",u"庙",u"陷",u"旺"]
WQMX = [u"庙",u"庙",u"平",u"旺",u"庙",u"庙",u"陷",u"旺",u"平",u"庙",u"陷",u"旺"]
LCMX = [u"旺",u"",u"庙",u"旺",u"",u"庙",u"旺",u"",u"庙",u"旺",u"",u"庙"]
TMMX = [u"",u"",u"旺",u"",u"",u"平",u"",u"",u"旺",u"",u"",u"平"]
FuYaoMX=[ZFMX,YBMX,WQMX,WCMX,TKMX,TYueMX,LCMX,TMMX]

HLMX = [u"平",u"庙",u"平",u"陷",u"庙",u"地",u"平",u"庙",u"庙",u"平",u"庙",u"庙"]
HQMX = [u"闲",u"庙",u"旺",u"旺",u"平",u"平",u"庙",u"旺",u"旺",u"平",u"庙",u"旺"]
HKMX = [u"旺",u"旺",u"旺",u"庙",u"庙",u"闲",u"庙",u"旺",u"庙",u"平",u"旺",u"旺"]
HJMX = [u"旺",u"庙",u"陷",u"旺",u"闲",u"陷",u"陷",u"旺",u"陷",u"陷",u"陷",u"陷"]
HuaYaoMX = [HLMX,HQMX,HKMX,HJMX]

QYMX = [u"陷",u"庙",u"",u"陷",u"庙",u"",u"平",u"庙",u"",u"陷",u"庙",u""]
TLumx = [u"",u"庙",u"陷",u"",u"庙",u"陷",u"",u"庙",u"陷",u"",u"庙",u"陷"]
HXMX = [u"平",u"旺",u"庙",u"平",u"闲",u"旺",u"庙",u"闲",u"陷",u"陷",u"庙",u"平"]
LXMX = [u"陷",u"陷",u"庙",u"庙",u"旺",u"旺",u"庙",u"旺",u"旺",u"陷",u"庙",u"庙"]
DKMX = [u"平",u"陷",u"陷",u"平",u"陷",u"庙",u"庙",u"平",u"庙",u"庙",u"陷",u"陷"]
DJMX = [u"陷",u"陷",u"平",u"平",u"陷",u"闲",u"庙",u"平",u"庙",u"平",u"平",u"旺"]
ShaYaoMX = [HXMX,LXMX,QYMX,TLumx]
KongYaoMX = [DJMX,DKMX,['']*12]

def paipan(lyear,lmonth,lday,leap,ygindex,yzindex,hzindex,sex):
    print lyear,lmonth,lday,leap,ygindex,yzindex,hzindex
    '寅宫起正月顺数至生月，再从该宫起子时，逆数至本生时为命宫；由本生月宫位顺数至本生时为身宫'
    mgindex = (lmonth-1-hzindex+12+2)% 12
    sgindex = (lmonth-1+hzindex+12+2)% 12
    print u'命宫',mgindex,Dizhi[mgindex]
    print u'身宫',sgindex,Dizhi[sgindex]
    gwgan = [-1]*12
    gwzhi = [-1]*12
    for i in range(0,12):
        '命宫逆排安十二宫位支'
        gwzhi[i] = (mgindex-i+12) % 12
        '甲己在寅宫起丙，乙庚在寅宫起戊，丙辛在寅宫起庚，丁壬在寅宫起壬，戊癸在寅宫起甲顺排天干'
        gwgan[i] = (gwzhi[i]+2*(ygindex%5)) %10
        if sgindex == gwzhi[i]:
            sgganindex = gwgan[i]
        print GongWei[i],Tiangan[gwgan[i]],Dizhi[gwzhi[i]]
    print gwzhi
    '定五行局'
    print Tiangan[gwgan[0]]+Dizhi[gwzhi[0]]
    wh = NaYin.get(Tiangan[gwgan[0]]+Dizhi[gwzhi[0]])[2]
    whju =  WhJu[wh]
    whindex = WhJuIndex[wh]
    '起大限'
    dxfrom = [-1]*12
    dxto = [-1]*12
    for i in range(0,12):
        dxfrom[i] = whindex+i*10
        dxto[i] = dxfrom[i]+9
        print dxfrom[i],"~",dxto[i]
    '起紫薇星'
    yu = lday % whindex
    shang = lday / whindex
    if wh == u"火" and yu == 1:
        zwindex = (9 + shang)% 12  #酉
    elif (wh == u"火" and yu == 2) or (wh == u"土" and yu == 1):
        zwindex = (6 + shang)% 12  #午
    elif (wh == u"火" and yu == 3) or (wh == u"土" and yu == 2) or (wh == u"金" and yu == 1):
        zwindex = (11 + shang)% 12  #亥
    elif (wh == u"火" and yu == 4) or (wh == u"土" and yu == 3) or (wh == u"金" and yu == 2) or (wh == u"木" and yu == 1):
        zwindex = (4 + shang)% 12  #辰
    elif (wh == u"火" and yu == 5) or (wh == u"土" and yu == 4) or (wh == u"金" and yu == 3) or (wh == u"木" and yu == 2) or (wh == u"水" and yu == 1):
        zwindex = (1 + shang)% 12  #丑
    elif yu == 0:
        zwindex = (2 + shang)% 12  #寅
    '起天府星'
    if zwindex < 5 :
        tfindex = 4 - zwindex
    elif zwindex >=5 :
        tfindex = 16 - zwindex
    '天机，太阳，武曲，天同，廉贞'
    tjindex,tyindex,wuqindex,ttindex,lzindex = (zwindex - 1)%12,(zwindex - 3)%12,(zwindex - 4)%12,(zwindex - 5)%12,(zwindex +4)%12
    '太阴，贪狼，巨门，天相，天梁，七杀，破军'
    tyiindex,tlindex,jmindex,txaindex,tliindex,qsindex,pjindex = (tfindex + 1)% 12,(tfindex + 2)% 12,(tfindex + 3)% 12,(tfindex + 4)% 12,(tfindex + 5)% 12,(tfindex + 6)% 12,(tfindex - 2)% 12
    print "紫薇:%s,天机:%s,太阳:%s,武曲:%s,天同:%s,廉贞:%s"% (Dizhi[zwindex],Dizhi[tjindex],Dizhi[tyindex],Dizhi[wuqindex],Dizhi[ttindex],Dizhi[lzindex])
    print "天府:%s,太阴:%s,贪狼:%s,巨门:%s,天相:%s,天梁:%s,七杀:%s,破军:%s" % (Dizhi[tfindex],Dizhi[tyiindex],Dizhi[tlindex],Dizhi[jmindex],Dizhi[txaindex],Dizhi[tliindex],Dizhi[qsindex],Dizhi[pjindex])
    '左辅右弼 辰顺戌逆月份'
    zfindex,ybindex = (4 + lmonth-1) % 12,(10 - lmonth+1) % 12
    '文曲文昌 辰顺戌逆时辰'
    wqindex,wcindex = (4 + hzindex) % 12,(10 - hzindex) % 12
    '地劫地空 亥顺逆时辰'
    djindex,dkindex = (11 + hzindex) % 12,(11 - hzindex) % 12
    '看年干'
    '生年四化 甲廉破武阳，乙机梁紫阴，丙同机昌廉，丁阴同机巨，戊贪阴阳机，己武贪梁曲，庚阳武府同，辛巨阳曲昌，壬梁紫府武，癸破巨阴贪'
    '禄存，羊陀'
    '天官，天福，天厨'
    '截空'
    if ygindex == 0:
        snhlindex,snhqindex,snhkindex,snhjindex,snhl,snhq,snhk,snhj = lzindex,pjindex,wuqindex,tyindex,u"廉贞",u"破军",u"武曲",u"太阳"
        tluindex,lcindex,qyindex = 1,2,3
        tgindex,tfuindex,tcindex = 7,9,5
        zkindex,bkindex = 8,9
    elif ygindex == 1:
        snhlindex,snhqindex,snhkindex,snhjindex,snhl,snhq,snhk,snhj = tjindex,tliindex,zwindex,tyiindex,u"天机",u"天梁",u"紫薇",u"太阴"
        tluindex,lcindex,qyindex = 2,3,4
        tgindex,tfuindex,tcindex = 4,8,6
        zkindex,bkindex = 7,6
    elif ygindex == 2:
        snhlindex,snhqindex,snhkindex,snhjindex,snhl,snhq,snhk,snhj = ttindex,tjindex,wcindex,lzindex,u"天同",u"天机",u"文昌",u"廉贞"
        tluindex,lcindex,qyindex = 4,5,6
        tgindex,tfuindex,tcindex = 5,0,0
        zkindex,bkindex = 4,5
    elif ygindex == 3:
        snhlindex,snhqindex,snhkindex,snhjindex,snhl,snhq,snhk,snhj = tyiindex,ttindex,tjindex,jmindex,u"太阴",u"天同",u"天机",u"巨门"
        tluindex,lcindex,qyindex = 5,6,7
        tgindex,tfuindex,tcindex = 2,11,5
        zkindex,bkindex = 3,2
    elif ygindex == 4:
        snhlindex,snhqindex,snhkindex,snhjindex,snhl,snhq,snhk,snhj = tlindex,tyiindex,tyindex,tjindex,u"贪狼",u"太阴",u"太阳",u"天机"
        tluindex,lcindex,qyindex = 4,5,6
        tgindex,tfuindex,tcindex = 3,3,6
        zkindex,bkindex = 0,1
    elif ygindex == 5:
        snhlindex,snhqindex,snhkindex,snhjindex,snhl,snhq,snhk,snhj = wuqindex,tlindex,tliindex,wqindex,u"武曲",u"贪狼",u"天梁",u"文曲"
        tluindex,lcindex,qyindex = 5,6,7
        tgindex,tfuindex,tcindex = 9,2,9
        zkindex,bkindex = 9,8
    elif ygindex == 6:
        snhlindex,snhqindex,snhkindex,snhjindex,snhl,snhq,snhk,snhj = tyindex,wuqindex,tfindex,ttindex,u"太阳",u"武曲",u"天府",u"天同"
        tluindex,lcindex,qyindex = 7,8,9
        tgindex,tfuindex,tcindex = 11,6,2
        zkindex,bkindex = 6,7
    elif ygindex == 7:
        snhlindex,snhqindex,snhkindex,snhjindex,snhl,snhq,snhk,snhj = jmindex,tyindex,wqindex,wcindex,u"巨门",u"太阳",u"文曲",u"文昌"
        tluindex,lcindex,qyindex = 8,9,10
        tgindex,tfuindex,tcindex = 9,5,6
        zkindex,bkindex = 5,4
    elif ygindex == 8:
        snhlindex,snhqindex,snhkindex,snhjindex,snhl,snhq,snhk,snhj = tliindex,zwindex,tfindex,wuqindex,u"天梁",u"紫薇",u"天府",u"武曲"
        tluindex,lcindex,qyindex = 10,11,0
        tgindex,tfuindex,tcindex = 10,6,9
        zkindex,bkindex = 2,3
    elif ygindex == 9:
        snhlindex,snhqindex,snhkindex,snhjindex,snhl,snhq,snhk,snhj = pjindex,jmindex,tyiindex,tlindex,u"破军",u"巨门",u"太阴",u"贪狼"
        tluindex,lcindex,qyindex = 11,0,1
        tgindex,tfuindex,tcindex = 6,5,11
        zkindex,bkindex = 1,0
    '魁钺'
    if ygindex == 0 or ygindex ==4 or ygindex == 6:
        tkindex,tyueindex = 1,7
    elif ygindex == 1 or ygindex == 5:
        tkindex,tyueindex = 0,8
    elif ygindex == 2 or ygindex == 3:
        tkindex,tyueindex = 11,9
    elif ygindex == 8 or ygindex == 9:
        tkindex,tyueindex = 3,5
    elif ygindex == 7:
        tkindex,tyueindex = 6,2
    '看年支'
    '火铃'
    '天马'
    '劫煞'
    '华盖，咸池'
    if yzindex == 0 or yzindex == 4 or yzindex == 8:  #申子辰
        hxindex,lxindex = (2+hzindex)%12,(10+hzindex)%12
        tmindex = 2
        jsindex = 5
        hzindex,xcindex = 4,9
    elif yzindex == 2 or yzindex == 6 or yzindex == 10: #寅午戌
        hxindex,lxindex = (1+hzindex)%12,(3+hzindex)%12
        tmindex = 8
        jsindex = 11
        hzindex,xcindex = 10,3
    elif yzindex == 1 or yzindex == 5 or yzindex == 9: #巳酉丑
        hxindex,lxindex = (3+hzindex)%12,(10+hzindex)%12
        tmindex = 11
        jsindex = 2
        hzindex,xcindex = 1,6
    elif yzindex == 3 or yzindex == 7 or yzindex == 11: #亥卯未
        hxindex,lxindex = (9+hzindex)%12,(10+hzindex)%12
        tmindex = 5
        jsindex = 8
        hzindex,xcindex = 7,0
    '年前一支为天空'
    tkoindex = (yzindex+1) %12
    '天哭天虚'
    tkuindex,txuindex = (6-yzindex) % 12,(6+yzindex) % 12
    '红鸾天喜'
    hlindex,txindex = (3-yzindex) % 12,(9-yzindex) % 12
    '孤辰寡宿'
    if yzindex == 11 or yzindex == 0 or yzindex == 1:
        gcindex,gsindex = 2,10
    elif yzindex == 2 or yzindex == 3 or yzindex == 4:
        gcindex,gsindex = 5,1
    elif yzindex == 5 or yzindex == 6 or yzindex == 7:
        gcindex,gsindex = 8,4
    elif yzindex == 8 or yzindex == 9 or yzindex == 10:
        gcindex,gsindex = 11,7
    '大耗'
    '蜚廉，破碎，龙德，月德'
    if yzindex == 0:
        dhindex = 7
        flindex,psindex,ldindex,ydindex = 8,5,7,5
    elif yzindex == 1:
        dhindex = 6
        flindex,psindex,ldindex,ydindex = 9,1,8,6
    elif yzindex == 2:
        dhindex = 9
        flindex,psindex,ldindex,ydindex = 10,9,9,7
    elif yzindex == 3:
        dhindex = 8
        flindex,psindex,ldindex,ydindex = 5,5,10,8
    elif yzindex == 4:
        dhindex = 11
        flindex,psindex,ldindex,ydindex = 6,1,11,9
    elif yzindex == 5:
        dhindex = 10
        flindex,psindex,ldindex,ydindex = 7,9,0,10
    elif yzindex == 6:
        dhindex = 1
        flindex,psindex,ldindex,ydindex = 2,5,1,11
    elif yzindex == 7:
        dhindex = 0
        flindex,psindex,ldindex,ydindex = 3,1,2,0
    elif yzindex == 8:
        dhindex = 3
        flindex,psindex,ldindex,ydindex = 4,9,3,1
    elif yzindex == 9:
        dhindex = 2
        flindex,psindex,ldindex,ydindex = 11,5,4,2
    elif yzindex == 10:
        dhindex = 5
        flindex,psindex,ldindex,ydindex = 0,1,5,3
    elif yzindex == 11:
        dhindex = 4
        flindex,psindex,ldindex,ydindex = 1,9,6,4
    '天德，年解'
    tdindex,njindex = (9+yzindex)%12,(10-yzindex)%12
    '天才天寿'
    tciindex,tshindex = (mgindex+yzindex)%12,(sgindex+yzindex)%12
    '龙池凤阁'
    lchindex,fgeindex = (4+yzindex) % 12,(10-yzindex) % 12
    '台辅封诰'
    tafuindex,fgindex = (wqindex + 2) % 12,(wqindex - 2) % 12
    '天刑天姚'
    txiindex,tyaindex = (9+lmonth-1)% 12,(1+lmonth-1)% 12
    '解神天巫'
    '天月阴煞'
    if lmonth == 1:
        jshindex,twuindex = 8,5
        tyuindex,yshindex = 10,2
    elif lmonth == 2:
        jshindex,twuindex = 8,8
        tyuindex,yshindex = 5,0
    elif lmonth == 3:
        jshindex,twuindex = 10,2
        tyuindex,yshindex = 4,10
    elif lmonth == 4:
        jshindex,twuindex = 10,11
        tyuindex,yshindex = 2,8
    elif lmonth == 5:
        jshindex,twuindex = 0,5
        tyuindex,yshindex = 7,6
    elif lmonth == 6:
        jshindex,twuindex = 0,8
        tyuindex,yshindex = 3,4
    elif lmonth == 7:
        jshindex,twuindex = 2,2
        tyuindex,yshindex = 11,2
    elif lmonth == 8:
        jshindex,twuindex = 2,11
        tyuindex,yshindex = 7,0
    elif lmonth == 9:
        jshindex,twuindex = 4,5
        tyuindex,yshindex = 2,10
    elif lmonth == 10:
        jshindex,twuindex = 4,8
        tyuindex,yshindex = 6,8
    elif lmonth == 11:
        jshindex,twuindex = 6,2
        tyuindex,yshindex = 10,6
    elif lmonth == 12:
        jshindex,twuindex = 6,11
        tyuindex,yshindex = 2,4
    '天伤天使'
    '三台八座'
    stindex,bzindex = (zfindex + lday-1) % 12, (ybindex - lday+1) % 12
    '恩光天贵'
    eginidex,tguindex = (wcindex + lday-2) % 12,(wqindex + lday-2) % 12
    '命主,身主，流曲流昌'
    '长生十二神'
    csindex = [-1]*12
    if whindex == 2 or whindex == 5:
        csstart = 8
    elif whindex == 3:
        csstart = 11
    elif whindex == 4:
        csstart = 5
    elif whindex == 6:
        csstart = 2
    if (ygindex%2) ^ (sex == u"男"):
        shun = 1
        for i in range(0,12):
            csindex[i] = (csstart + i)%12
    else:
        shun = 0
        for i in range(0,12):
            csindex[i] = (csstart - i)%12
    '太岁十二神'
    tsindex = [-1]*12
    for i in range(0,12):
        tsindex[i] = (yzindex + i) % 12
    '将前十二神'
    jqindex = [-1]*12
    if yzindex == 0 or yzindex == 4 or yzindex == 8:  #申子辰
        jqstart = 0
    elif yzindex == 2 or yzindex == 6 or yzindex == 10: #寅午戌
        jqstart = 6
    elif yzindex == 1 or yzindex == 5 or yzindex == 9: #巳酉丑
        jqstart = 9
    elif yzindex == 3 or yzindex == 7 or yzindex == 11: #亥卯未
        jqstart = 3
    for i in range(0,12):
        jqindex[i] = (jqstart + i) % 12
    '博士十二神'
    bsindex = [-1]*12
    if shun == 1:
        for i in range(0,12):
            bsindex[i] = (lcindex + i) % 12
    else:
        for i in range(0,12):
            bsindex[i] = (lcindex - i) % 12

    zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12 = collections.OrderedDict(),collections.OrderedDict(),collections.OrderedDict(),collections.OrderedDict(),collections.OrderedDict(),collections.OrderedDict(),collections.OrderedDict(),collections.OrderedDict(),collections.OrderedDict(),collections.OrderedDict()
    zhengyao[u"紫薇"],zhengyao[u"天府"],zhengyao[u"天机"],zhengyao[u"太阳"],zhengyao[u"武曲"],zhengyao[u"天同"],zhengyao[u"廉贞"]=zwindex,tfindex,tjindex,tyindex,wuqindex,ttindex,lzindex
    zhengyao[u"太阴"],zhengyao[u"贪狼"],zhengyao[u"巨门"],zhengyao[u"天相"],zhengyao[u"天梁"],zhengyao[u"七杀"],zhengyao[u"破军"]=tyiindex,tlindex,jmindex,txaindex,tliindex,qsindex,pjindex
    fuyao[u"左辅"],fuyao[u"右弼"],fuyao[u"文曲"],fuyao[u"文昌"],fuyao[u"天魁"],fuyao[u"天钺"],fuyao[u"禄存"],fuyao[u"天马"]=zfindex,ybindex,wqindex,wcindex,tkindex,tyueindex,lcindex,tmindex
    shayao[u"火星"],shayao[u"铃星"],shayao[u"擎羊"],shayao[u"陀罗"]=hxindex,lxindex,qyindex,tluindex
    huayao[u"化禄"],huayao[u"化权"],huayao[u"化科"],huayao[u"化忌"]=(snhlindex,snhl),(snhqindex,snhq),(snhkindex,snhk),(snhjindex,snhj)
    kongyao[u"地劫"],kongyao[u"地空"],kongyao[u"天空"]=djindex,dkindex,tkoindex
    '杂曜'
    zayao[u"天官"],zayao[u"天福"],zayao[u"天厨"],zayao[u"正空"],zayao[u"傍空"],zayao[u"劫煞"]=tgindex,tfuindex,tcindex,zkindex,bkindex,jsindex
    zayao[u"华盖"],zayao[u"咸池"],zayao[u"天哭"],zayao[u"天虚"],zayao[u"红鸾"],zayao[u"天喜"]=hzindex,xcindex,tkuindex,txuindex,hlindex,txindex
    zayao[u"孤辰"],zayao[u"寡宿"],zayao[u"大耗"],zayao[u"蜚廉"],zayao[u"破碎"],zayao[u"龙德"],zayao[u"月德"]=gcindex,gsindex,dhindex,flindex,psindex,ldindex,ydindex
    zayao[u"天德"],zayao[u"年解"],zayao[u"天才"],zayao[u"天寿"],zayao[u"龙池"],zayao[u"凤阁"],zayao[u"台辅"],zayao[u"封诰"]=tdindex,njindex,tciindex,tshindex,lchindex,fgeindex,tafuindex,fgindex
    zayao[u"天刑"],zayao[u"天姚"],zayao[u"解神"],zayao[u"天巫"],zayao[u"天月"],zayao[u"阴煞"],zayao[u"三台"],zayao[u"八座"],zayao[u"恩光"],zayao[u"天贵"]=txiindex,tyaindex,jshindex,twuindex,tyuindex,yshindex,stindex,bzindex,eginidex,tguindex
    '长生十二神'
    for i in range(0,12):
        changsheng12[CSXingYao[i]] = csindex[i]
    '太岁十二神'
    for i in range(0,12):
        changsheng12[TSXingYao[i]] = tsindex[i]
    '将前十二神'
    for i in range(0,12):
        jiangqian12[JQXingYao[i]] = jqindex[i]
    '博士十二神'
    for i in range(0,12):
        boshi12[BSXingYao[i]] = bsindex[i]

    return mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12

def save_paipan(selsql='select id,sex,lyear,lmonth,lday,leap,ygindex,yzindex,hzindex from mingzhu'
                ,updsql="delete from ziwei where pid=%d;insert into ziwei(pid,whindex,whju,mggan,mgzhi,sggan,sgzhi,xdggan,xdgzhi,fqggan \
                ,fqgzhi,znggan,zngzhi,cbggan,cbgzhi,jeggan,jegzhi,qyggan,qygzhi,jyggan \
                ,jygzhi,syggan,sygzhi,tzggan,tzgzhi,fdggan,fdgzhi,fmggan,gmgzhi,mggindex \
                ,mgzindex,sggindex,sgzindex,xdggindex,xdgzindex,fqggindex,fqgzindex,znggindex,zngzindex,cbggindex \
                ,cbgzindex,jeggindex,jegzindex,qyggindex,qygzindex,jyggindex,jygzindex,syggindex,sygzindex,tzggindex \
                ,tzgzindex,fdggindex,fdgzindex,fmggindex,fmgzindex) \
                values(%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s' \
                ,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'\
                ,'%s','%s','%s','%s','%s','%s','%s','%s','%s',%d \
                ,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d \
                ,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d \
                ,%d,%d,%d,%d,%d)"
                ,delsql = "delete from xingyao where pid=%d;"
                ,updxysql = "insert into xingyao(pid,xingyao,miaoxian,type,zhi,zhiindex) values(%d,'%s','%s',%d,'%s',%d)"
                ,updhxysql = "insert into xingyao(pid,xingyao,huaxingyao,miaoxian,type,zhi,zhiindex) values(%d,'%s','%s','%s',%d,'%s',%d)"):
    results=sh.ExecQuery(selsql)
    for result in results:
        try:
            id,sex,lyear,lmonth,lday,leap,ygindex,yzindex,hzindex=result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8]
            mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12 = paipan(lyear,lmonth,lday,leap,ygindex,yzindex,hzindex,sex)
            sql = updsql % (id,id,whindex,whju,Tiangan[gwgan[0]],Dizhi[gwzhi[0]],Tiangan[sgganindex],Dizhi[sgindex],Tiangan[gwgan[1]],Dizhi[gwzhi[1]],Tiangan[gwgan[2]]
                            ,Dizhi[gwzhi[2]],Tiangan[gwgan[3]],Dizhi[gwzhi[3]],Tiangan[gwgan[4]],Dizhi[gwzhi[4]],Tiangan[gwgan[5]],Dizhi[gwzhi[5]],Tiangan[gwgan[6]],Dizhi[gwzhi[6]],Tiangan[gwgan[7]]
                            ,Dizhi[gwzhi[7]],Tiangan[gwgan[8]],Dizhi[gwzhi[8]],Tiangan[gwgan[9]],Dizhi[gwzhi[9]],Tiangan[gwgan[10]],Dizhi[gwzhi[10]],Tiangan[gwgan[11]],Dizhi[gwzhi[11]],gwgan[0]
                            ,gwzhi[0],sgganindex,mgindex, gwgan[1],gwzhi[1],gwgan[2],gwzhi[2],gwgan[3],gwzhi[3],gwgan[4]
                            ,gwzhi[4],gwgan[5],gwzhi[5],gwgan[6],gwzhi[6],gwgan[7],gwzhi[7],gwgan[8],gwzhi[8],gwgan[9]
                            ,gwzhi[9],gwgan[10],gwzhi[10],gwgan[11],gwzhi[11])
            sql = delsql % (id);
            sh.ExecNonQuery(sql)
            i=0
            for k,v in zhengyao.items():
                sql = updxysql % (id,k,ZhengYaoMX[i][v],1,Dizhi[v],v);
                i+=1
                sh.ExecNonQuery(sql)
            i=0
            for k,v in fuyao.items():
                sql = updxysql % (id,k,FuYaoMX[i][v],2,Dizhi[v],v);
                i+=1
                sh.ExecNonQuery(sql)
            i=0
            for k,v in shayao.items():
                sql = updxysql % (id,k,ShaYaoMX[i][v],3,Dizhi[v],v);
                i+=1
                sh.ExecNonQuery(sql)
            i=0
            for k,v in huayao.items():
                sql = updhxysql % (id,k,v[1],HuaYaoMX[i][v[0]],4,Dizhi[v[0]],v[0]);
                i+=1
                sh.ExecNonQuery(sql)
            i=0
            for k,v in kongyao.items():
                sql = updxysql % (id,k,KongYaoMX[i][v],5,Dizhi[v],v);
                i+=1
                sh.ExecNonQuery(sql)
            for k,v in zayao.items():
                sql = updxysql % (id,k,'',6,Dizhi[v],v);
                sh.ExecNonQuery(sql)
            for k,v in changsheng12.items():
                sql = updxysql % (id,k,'',7,Dizhi[v],v);
                sh.ExecNonQuery(sql)
            for k,v in taisui12.items():
                sql = updxysql % (id,k,'',8,Dizhi[v],v);
                sh.ExecNonQuery(sql)
            for k,v in jiangqian12.items():
                sql = updxysql % (id,k,'',9,Dizhi[v],v);
                sh.ExecNonQuery(sql)
            for k,v in boshi12.items():
                sql = updxysql % (id,k,'',10,Dizhi[v],v);
                sh.ExecNonQuery(sql)
        except Exception,e:
            print 'error:',e.message,traceback.format_exc()

if __name__ == '__main__':
    '''
    dt=datetime.datetime(year=1977,month=1,day=6,hour=1,minute=15)
    sex = u"女"
    bz=Bazi.bazi(dt,sex==u'女')
    bz.Paipan()
    lyear,lmonth,lday,leap = bz.Solar2Lunar(dt)
    ygindex,yzindex,hzindex = bz.bazi[0],bz.bazi[1],bz.bazi[7]
    mgindex,sgindex,whindex,whju,sgganindex,sgindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12 =  paipan(lyear,lmonth,lday,leap,ygindex,yzindex,hzindex,sex)
    print zhengyao
    '''
    save_paipan()









