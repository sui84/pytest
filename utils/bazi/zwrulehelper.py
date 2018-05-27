#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
from utils.db import sqlhelper
from utils import setting
import datetime
import Bazi
import traceback
import ziweihelper
mysqldb = setting.YAMLDATA.get('mysqldb2')
host,user,pwd,db=mysqldb.get('host'),mysqldb.get('user'),mysqldb.get('pwd'),mysqldb.get('bazidb')
sh=sqlhelper.SqlHelper(host,user,pwd,db,'mysql')
'''
八喜楼钞本
太微赋
形体赋
'''


def kongwei(zindex,zhengyaos):
    print zindex,zhengyaos
    for k,v in zhengyaos.items():
        if zindex == v:
            return False
    return True

def shaji(zindex,xingji,cnt):
    insfsz = 0
    for xj in xingji:
        if xj in sfsz(zindex):
            insfsz+=1
    if insfsz>=cnt:
        return True
    else:
        return False

def sfsz(zindex):
    '三方四正'
    return (zindex,(zindex+4)%12,(zindex+6)%12,(zindex+8)%12)

def xiangjia(zindex,zindex1,zindex2):
    if abs(zindex-zindex1)==1 and abs(zindex-zindex2)==1 and zindex1<>zindex2:
        return True
    else:
        return False

def baxl_rule(lyear,lmonth,lday,leap,ygindex,yzindex,hzindex,sex):
    '''
    dt=datetime.datetime(year=1956,month=1,day=5,hour=9,minute=15)
    sex = u"女"
    bz=Bazi.bazi(dt,sex==u'女')
    bz.Paipan()
    lyear,lmonth,lday,leap = bz.Solar2Lunar(dt)
    ygindex,yzindex,hzindex = bz.bazi[0],bz.bazi[1],bz.bazi[7]
    '''
    mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12 =  ziweihelper.paipan(lyear,lmonth,lday,leap,ygindex,yzindex,hzindex,sex)


    result = []
    result += ziwei_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += tianji_rule(sex,ygindex,yzindex,hzindex \
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += taiyang_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += wuqu_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += tiantong_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += lianzheng_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += tianfu_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += taiying_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += tanlang_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += jumen_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += tianxiang_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += tianliang_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += qisha_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += pojun_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += zuoyou_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += kuiyue_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += changqu_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += huayao_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    result += shayao_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)

    #for r in result:
    #    print r
    tw_result = []
    tw_result += tw_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)

    xt_result = []
    xt_result += xt_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12)
    return result,tw_result,xt_result

def tw_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    if mgindex == zhengyao[u"破军"] or mgindex == zhengyao[u"七杀"]:
        if huayao[u"化忌"][0] in sfsz(mgindex) and huayao[u"化忌"][1]  in (u"廉贞",u"武曲",u"文曲"):
            result.append (u"七杀破军不喜廉贞化忌，武曲化忌，破军独不喜文曲化忌，若更见煞曜，凶难灾险重重")
    if (zhengyao[u"太阳"] ==10 and zhengyao[u"太阴"] == 4) or (zhengyao[u"太阳"] ==11 and zhengyao[u"太阴"] == 3):
            result.append (u"日月反背")
    if (ygindex == 1 and mgindex == zhengyao[u"天机"] and zhengyao[u"天机"]==11) or (ygindex == 3 and mgindex == 9 and zhengyao[u"天机"]==3) \
        or (ygindex == 5 and mgindex == zhengyao[u"武曲"] and zhengyao[u"武曲"]==1 and fuyao[u"文曲"]==5) \
        or (ygindex == 7 and mgindex == 4 and zhengyao[u"巨门"]==4 and fuyao[u"文昌"]==0):
        result.append (u"禄逢冲破吉成凶")
    if zayao[u"正空"] ==  fuyao[u"天马"] and fuyao[u"天马"] in sfsz(mgindex):
        result.append (u"马遇空亡主奔波")
    wh = ziweihelper.NaYin.get(ziweihelper.Tiangan[gwgan[0]]+ziweihelper.Dizhi[gwzhi[0]])[2]
    if (wh == u'金' and mgindex ==6 ) or (wh == u'木' and mgindex ==0 ) or (wh == u'水' and mgindex ==9 ) or (wh == u'火' and mgindex ==3 ):
        result.append (u"生逢败地，发也虚花。须得动曜并且见刑煞")
    if mgindex == zhengyao[u"贪狼"] and shayao[u"火星"] in sfsz(mgindex) and zhengyao[u"武曲"] in sfsz(mgindex)  and huayao[u"化禄"][1] == u"武曲":
        result.append (u"火贪格最喜武曲化禄")
    if mgindex == zhengyao[u"紫薇"] and zhengyao[u"紫薇"] == zhengyao[u"破军"] and xiangjia(zhengyao[u"紫薇"],fuyao[u"左辅"],fuyao[u"右弼"]):
        result.append (u"辅弼夹帝增加了安定")
    if mgindex == zhengyao[u"紫薇"] and zhengyao[u"紫薇"] == zhengyao[u"贪狼"] and zayao[u"红鸾"] in sfsz(mgindex) and zayao[u"天喜"] in sfsz(mgindex) \
            and zayao[u"咸池"] in sfsz(mgindex) and zayao[u"大耗"] in sfsz(mgindex):
        result.append (u"情欲型的桃花犯主格局，若见文曲文昌更加桃花，再见煞忌，则沦为下流。若见天刑天空截空，为制化")
    if (mgindex == zhengyao[u"紫薇"] and zhengyao[u"紫薇"] == zhengyao[u"天相"] and fuyao[u"文曲"] in sfsz(mgindex) and fuyao[u"文昌"] in sfsz(mgindex)) \
        or (mgindex == zhengyao[u"天府"] and zhengyao[u"天府"] == 5) or (mgindex == zhengyao[u"紫薇"] and zhengyao[u"紫薇"] == zhengyao[u"破军"]):
        result.append (u"君臣庆会,才善经邦:紫相昌曲，同梁协府，辅弼夹帝")
    if fuyao[u"左辅"] in sfsz(mgindex) and fuyao[u"右弼"] in sfsz(mgindex) and fuyao[u"文曲"] in sfsz(mgindex) and fuyao[u"文昌"] in sfsz(mgindex) \
        and ((shayao[u"擎羊"] in sfsz(mgindex) and shayao[u"铃星"] in sfsz(mgindex))  or (kongyao[u"地劫"] in sfsz(mgindex) and kongyao[u"地空"] in sfsz(mgindex))):
        result.append (u"魁钺同行不喜冲破，见羊铃主痼疾，见空劫主不弟")
    if huayao[u"化禄"][0] in sfsz(mgindex) and huayao[u"化权"][0] in sfsz(mgindex) and huayao[u"化科"][0] in sfsz(mgindex) and fuyao[u"文曲"] in sfsz(mgindex) \
        and fuyao[u"文昌"] in sfsz(mgindex) and huayao[u"化忌"][0] not in sfsz(mgindex):
        result.append (u"禄文拱名，利科名")
    if huayao[u"化禄"][0] in sfsz(mgindex) and huayao[u"化权"][0] in sfsz(mgindex) and huayao[u"化科"][0] in sfsz(mgindex) and fuyao[u"文曲"] in sfsz(mgindex) \
        and fuyao[u"文昌"] in sfsz(mgindex) and huayao[u"化忌"][0]  in sfsz(mgindex):
        result.append (u"禄文拱名见忌，才高不遇")
    if mgindex == zhengyao[u"天府"] and xiangjia(mgindex,zhengyao[u"太阳"],zhengyao[u"太阴"]) and huayao[u"化禄"][1] in (u"天机",u"太阴"):
        result.append (u"日月夹财，不权则富")
    if ygindex == 2 and mgindex == 6 and shayao[u"擎羊"] == 6 and zhengyao[u"天同"] == 0:
        result.append (u"马头带剑，在外地建功立业")
    if ygindex == 2 and mgindex == 6 and shayao[u"擎羊"] == 6 and zhengyao[u"天同"] == 6:
        result.append (u"马头带剑反格，白手兴家却未必在外")
    if ygindex == 4 and mgindex == 6 and shayao[u"擎羊"] == 6 and zhengyao[u"贪狼"] == 6:
        result.append (u"马头带剑别格，白手兴家却未必在外")
    if mgindex == zhengyao[u"紫薇"] and zhengyao[u"紫薇"] == zhengyao[u"贪狼"] and huayao[u"化忌"][0] == zhengyao[u"贪狼"] and kongyao[u"地空"] in sfsz(mgindex):
        result.append (u"桃花犯主意义改变，好哲学或艺术，若见火陀或羊铃，主科名不利")
    if mgindex == 6 and zhengyao[u"廉贞"] == zhengyao[u"天相"] and ygindex == 3 and zhengyao[u"天相"] == 6:
        result.append (u"刑忌夹印，每六年有官非")
    if mgindex == zhengyao[u"天同"] and mgindex in (4,10) and zhengyao[u"天梁"] in (0,6) and zhengyao[u"天机"] == zhengyao[u"太阴"] \
            and zhengyao[u"天机"] in (2,8):
        result.append (u"善荫朝纲，善慈之长")
    if gwzhi[4] in (zhengyao[u"天府"],zhengyao[u"武曲"],zhengyao[u"太阴"]) and (huayao[u"化禄"] in sfsz(mgindex) or fuyao[u"禄存"] in sfsz(mgindex)):
        result.append (u"财居财位，遇者富奢")
    if zhengyao[u"太阳"] == 6 and (huayao[u"化禄"] in sfsz(mgindex) or fuyao[u"禄存"] in sfsz(mgindex)) and (fuyao[u"文曲"] in sfsz(mgindex) or fuyao[u"文昌"] in sfsz(mgindex)):
        result.append (u"日丽中天，重视文曜")
    if mgindex == zhengyao[u"紫薇"] and  zhengyao[u"紫薇"] ==  zhengyao[u"破军"] and (huayao[u"化禄"] in sfsz(mgindex) or fuyao[u"禄存"] in sfsz(mgindex)):
        result.append (u"紫薇破军须辅弼，破军最喜化禄")
    if ygindex in (2,3) and zhengyao[u"太阴"] == 0 and zhengyao[u"天同"]==0 and zhengyao[u"太阴"] in (mgindex,sgindex):
        result.append (u"若会文昌则是阳梁昌禄格，最怕天虚，火星，大耗，天使等")
    if fuyao[u"文曲"] == zhengyao[u"破军"]  and zhengyao[u"破军"] in (2,3) and mgindex == zhengyao[u"破军"]:
        result.append (u"暗耗组合主耗散，见刑煞文曲多惊险反覆，见禄则终有成不致终身辛苦")
    if mgindex == zhengyao[u"太阴"] and zhengyao[u"太阳"] == zhengyao[u"太阴"]:
        result.append (u"日月守命不如合照")
    if mgindex == 7 and zhengyao[u"太阳"] == 3 and zhengyao[u"太阴"] == 11:
        result.append (u"少年科第")
    if mgindex == 1 and zhengyao[u"太阳"] == 9 and zhengyao[u"太阴"] == 5:
        result.append (u"纵有科名亦迟，而且人生较孤，尤主男女感情的痛苦")
    if mgindex == 7 and zhengyao[u"太阳"] == 11 and zhengyao[u"太阴"] == 3:
        result.append (u"孤苦多难，日月合照看明暗")
    if zhengyao[u"天同"] == zhengyao[u"天梁"] and mgindex == zhengyao[u"天梁"]:
        result.append (u"荫福聚会不怕凶厄。")
    if zhengyao[u"天同"] == zhengyao[u"天梁"] and mgindex == zhengyao[u"天梁"] and (shayao[u"铃星"] in sfsz(mgindex) or shayao[u"陀罗"] in sfsz(mgindex)):
        result.append (u"荫福聚会但所遇凶危更大，逢魁钺可减轻凶危。")
    if zhengyao[u"天同"] == zhengyao[u"天梁"] and mgindex == zhengyao[u"天梁"] and huayao[u"化科"][1] == u"天梁":
        result.append (u"荫福聚会，天梁化科主声望。")
    if mgindex == zhengyao[u"贪狼"] and zhengyao[u"贪狼"] == 0 and zhengyao[u"贪狼"] == shayao[u"擎羊"]:
        result.append (u"泛水桃花，武曲化忌使全盘格局严重的缺点。若有吉曜，亦主艺术。主要指女命")
    if mgindex == zhengyao[u"贪狼"] and zhengyao[u"贪狼"] == 11 and zhengyao[u"贪狼"] == shayao[u"陀罗"]:
        result.append (u"泛水桃花，天府无禄婚姻不美。若有吉曜，亦主艺术。主要指女命")
    if mgindex == zhengyao[u"贪狼"] and zhengyao[u"贪狼"] == 2 and zhengyao[u"贪狼"] == shayao[u"陀罗"] and \
            (zhengyao[u"贪狼"] == shayao[u"火星"] or zayao[u"天刑"] in sfsz(mgindex)):
        result.append (u"风流采杖主聪明，因色惹祸.发动之期在大限流年羊陀冲起的年份。主要指男命")
    if mgindex == zhengyao[u"廉贞"] and zhengyao[u"廉贞"] == zhengyao[u"破军"] and mgindex == 9:
        result.append (u"若武曲，廉贞皆化为忌星相冲,则血光的意味很重")
    if mgindex == zhengyao[u"破军"] and mgindex in (11,0,1) and zhengyao[u"破军"] == fuyao[u"文曲"] and huayao[u"化忌"][0] in sfsz(mgindex):
        result.append (u"破军暗曜共水乡，武曲破军最劣，九死一生")
    if mgindex == zhengyao[u"贪狼"] and mgindex in (1,7) and zhengyao[u"贪狼"] == fuyao[u"文曲"]:
        result.append (u"二曲贪狼，若见虚耗阴煞，主自杀倾向")
    if fuyao[u"禄存"] == gwzhi[7]:
        result.append (u"禄居奴仆主劳碌")
    if fuyao[u"文曲"] in sfsz(gwzhi[10]) and fuyao[u"文昌"] in sfsz(gwzhi[10]):
        result.append (u"昌曲最宜入福德宫，主人聪明，读书上进")
    if mgindex == zhengyao[u"太阳"] and  zhengyao[u"太阳"] == 3 and fuyao[u"文昌"] in sfsz(mgindex) and fuyao[u"禄存"] in sfsz(mgindex):
        result.append (u"阳梁昌禄，利功名")
    if zhengyao[u"太阳"] == 6 and zhengyao[u"太阳"] == gwzhi[8]:
        result.append (u"太阳文昌会于官禄宫利科名，在午宫容易沦为虚名虚位")
    if zhengyao[u"太阴"] == gwzhi[2] and zhengyao[u"太阴"] == fuyao[u"文曲"] and ziweihelper.TYiMX[zhengyao[u"太阴"]] == u"庙":
        result.append (u"太阴文曲会于妻宫，易得岳家提携")
    if fuyao[u"禄存"] in (gwzhi[4],gwzhi[9]):
        result.append (u"田宅宫见禄存主家富，财帛宫见禄存主身富，身富不如家富。化禄冲禄始应验")
    if fuyao[u"禄存"] == gwzhi[4] and zhengyao[u"太阴"] == gwzhi[9] and huayao[u"化禄"][0] == zhengyao[u"太阴"]:
        result.append (u"财帛宫见禄存有稳定收入，田宅宫最喜太阴化禄")
    if fuyao[u"禄存"] in sfsz(gwzhi[9]) and  huayao[u"化禄"][0] == zhengyao[u"太阴"] and zhengyao[u"太阴"] in sfsz(gwzhi[9]):
        result.append (u"田宅宫以太阴化禄叠禄存为佳")
    if  zhengyao[u"武曲"] == gwzhi[6] and huayao[u"化禄"][0] == zhengyao[u"武曲"] and fuyao[u"天马"] in sfsz(zhengyao[u"武曲"]):
        result.append (u"武曲禄马交驰，发财远部")
    if zhengyao[u"天梁"] == gwzhi[6] and zhengyao[u"天梁"] == 0:
        result.append (u"天梁逢吉曜，本地发财")
    if zhengyao[u"破军"] == gwzhi[8] and zhengyao[u"破军"] in (0,6) and huayao[u"化忌"][0] == zhengyao[u"廉贞"]:
        result.append (u"破军守事业宫，逢刑忌，主乞儿")
    if mgindex == zhengyao[u"贪狼"] and ((yzindex in (2,6,10) and zhengyao[u"贪狼"] == 6) or (yzindex in (1,5,9) and zhengyao[u"贪狼"] == 9) \
        or (yzindex in (3,7,11) and zhengyao[u"贪狼"] == 3) or (yzindex in (0,4,8) and zhengyao[u"贪狼"] == 0)):
        result.append (u"贪会旺宫物欲深")
    if zhengyao[u"贪狼"]  in sfsz(mgindex) and zhengyao[u"破军"]  in sfsz(mgindex) and zhengyao[u"七杀"] in sfsz(mgindex) and zhengyao[u"武曲"] == gwzhi[6]:
        result.append (u"杀破狼在三方相会且武曲在迁移宫，有不良倾向")
    if  zhengyao[u"七杀"] == mgindex and changsheng12[u"绝"] == mgindex:
        result.append (u"杀临绝地见煞刑，主人一生带疾")
    if zhengyao[u"贪狼"] == changsheng12[u"长生"] and ((yzindex in (2,6,10) and zhengyao[u"贪狼"] == 2) or (yzindex in (1,5,9) and zhengyao[u"贪狼"] == 5) \
        or (yzindex in (3,7,11) and zhengyao[u"贪狼"] == 11) or (yzindex in (0,4,8) and zhengyao[u"贪狼"] == 8)):
        result.append (u"贪坐生乡体魄强")
    xingjis = [shayao[u"火星"],shayao[u"铃星"],shayao[u"擎羊"],shayao[u"陀罗"],huayao[u"化忌"][0]]
    if shaji(gwzhi[6],xingjis,4)==True:
        result.append (u"迁移宫凶星会忌，身体遭伤")
    if shaji(gwzhi[11],xingjis,4)==True:
        result.append (u"父母宫凶星会忌，刑克父母")
    if shaji(gwzhi[8],xingjis,3)==True and zhengyao[u"廉贞"] == gwzhi[8]:
        result.append (u"刑煞会廉于官禄宫主官非，当流年官禄宫重叠，流煞忌重叠即有此克应")
    if kongwei(mgindex,zhengyao) == True and zhengyao[u"天机"] in sfsz(mgindex) and zhengyao[u"天同"] in sfsz(mgindex):
        result.append (u"善福守于空位，出家命")
    if kongwei(mgindex,zhengyao) and fuyao[u"左辅"] <> fuyao[u"右弼"] and mgindex in ( fuyao[u"左辅"],fuyao[u"右弼"]):
        result.append (u"辅弼单坐命，离宗庶出")
    if kongwei(mgindex,zhengyao) and shayao[u"火星"] <> shayao[u"铃星"] and mgindex in ( shayao[u"火星"],shayao[u"铃星"]):
        result.append (u"火铃单守命，两重父母")
    if zhengyao[u"七杀"] in (mgindex,sgindex):
        result.append (u"七杀临于身命，流年太岁刑忌并临，必主灾病官非")
    if huayao[u"化忌"][0] in sfsz(mgindex) and (mgindex == shayao[u"铃星"] and mgindex == shayao[u"擎羊"]) or (mgindex == shayao[u"陀罗"] and mgindex == shayao[u"火星"]):
        nianzhi = ziweihelper.Dizhi[(mgindex+8) % 12]
        result.append (u"命宫坐羊铃或陀火,又会刑忌,流年遇白虎须当刑戮."+nianzhi+u"年")
    return result


def xt_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    xingjis = [shayao[u"火星"],shayao[u"铃星"],shayao[u"擎羊"],shayao[u"陀罗"],huayao[u"化忌"][0]]
    if mgindex == zhengyao[u"紫薇"]:
        result.append (u"紫薇帝座，生为厚重之容")
        if mgindex == zhengyao[u"破军"] and shaji(mgindex,xingjis,3)==True:
            result.append (u"紫破，煞忌并见，主眼神游移不定")
        if mgindex == zhengyao[u"贪狼"]:
            result.append (u"紫贪，脸形带扁")
        if mgindex == zhengyao[u"七杀"]:
            result.append (u"紫杀，脸形带方，地阁额方")
        if mgindex == zhengyao[u"天府"]:
            result.append (u"紫府，脸形带扁面，或比紫杀更方")
        if fuyao[u"左辅"] in sfsz(mgindex) and fuyao[u"右弼"] in sfsz(mgindex):
            result.append (u"紫薇见辅弼，主观强而主见少，相貌必丰厚大方，双目慈和")
    if mgindex == zhengyao[u"天府"]:
        result.append (u"天府主方脸，多微胖或年老发胖。女命鼻多胆形")
        if huayao[u"化禄"] not in sfsz(mgindex) and  fuyao[u"禄存"] not in sfsz(mgindex) and shaji(mgindex,xingjis,3)==True:
            result.append (u"天府若无禄而刑煞重者，主瘦")
        if mgindex <> zhengyao[u"廉贞"]:
            result.append (u"天府与廉贞同度皮肤黄白")
        if mgindex == zhengyao[u"廉贞"]:
            result.append (u"天府皮肤粗黑")
    if mgindex == zhengyao[u"太阳"]:
        result.append (u"太阳面色红黄，红白，或带紫红")
        if ziweihelper.TYMX[mgindex] == u"庙":
            result.append (u"太阳入庙者圆脸")
        if ziweihelper.TYMX[mgindex] ==  u"陷":
            result.append (u"太阳落陷者带尖长")
        if zhengyao[u"太阳"] == huayao[u"化忌"][0]:
            result.append (u"太阳化忌主有眼疾,若见煞则双目一大一小或一高一低")
    if mgindex == zhengyao[u"太阴"]:
        result.append (u"太阴清奇，面色青白或青黄")
        if ziweihelper.TYiMX[mgindex] == u"庙":
            result.append (u"太阴入庙者圆而清秀")
        if ziweihelper.TYiMX[mgindex] ==  u"陷":
            result.append (u"太阴落陷者带尖薄")
        if ziweihelper.TYiMX[mgindex] ==  u"陷" and shaji(mgindex,xingjis,3)==True:
            result.append (u"太阴落陷见煞忌，色带青黑")
        if mgindex == zhengyao[u"天同"] and shaji(mgindex,xingjis,2)==True:
            result.append (u"天同太阴见煞，主鼻梁塌")
        if mgindex == zhengyao[u"天机"] and shaji(mgindex,xingjis,2)==True:
            result.append (u"太阴天机见煞忌，主双目高低大小")
    if mgindex == zhengyao[u"天机"]:
        result.append (u"天机面型长而带瘦，面色青白转为青黄")
        if ziweihelper.TJMX[mgindex] == u"庙":
            result.append (u"太机入庙者身长肥胖")
        if mgindex == zhengyao[u"巨门"]:
            result.append (u"天机巨门主瘦,目光浮泛")
        if mgindex == zhengyao[u"太阴"]:
            result.append (u"天机太阴,目光灵动")
        if mgindex == zhengyao[u"太梁"]:
            result.append (u"天机天梁,目光沉潜")
    if mgindex == zhengyao[u"武曲"]:
        result.append (u"武曲面型长圆，多带瘦。性果敢勇毅，有决断力")
        if mgindex == 3:
            result.append (u"武曲卯主体态肥胖")
        if mgindex in (5,10):
            result.append (u"武曲辰戌主身形瘦长")
    if mgindex == zhengyao[u"天同"]:
        result.append (u"天同圆方脸，面色黄白，或带微红。体态丰满，眼神仁慈")
        if mgindex == zhengyao[u"巨门"] and shayao[u"火星"]  in sfsz(mgindex) and shayao[u"铃星"]  in sfsz(mgindex):
            result.append (u"天同巨门同度，会火铃，主有异痣或胎记")
        if mgindex == zhengyao[u"太阴"] and mgindex ==0:
            result.append (u"女命天同太阴于子宫同度，眼神流丽")
    if mgindex == zhengyao[u"廉贞"]:
        result.append (u"廉贞眉宽，面横口阔.廉贞主露，眉露骨，颧露棱")
        if mgindex == zhengyao[u"天府"]:
            result.append (u"廉贞天府同度，脸色，肤色皆粗黑")
    if mgindex == zhengyao[u"贪狼"]:
        if ziweihelper.TLMX[zhengyao[u"贪狼"]] == u"庙":
            result.append (u"贪狼入庙则身躯肥满高大")
        if ziweihelper.TLMX[zhengyao[u"贪狼"]] == u"陷":
            result.append (u"贪狼落陷则形反主小")
        if ziweihelper.TLMX[zhengyao[u"贪狼"]] == u"陷" and shayao[u"擎羊"] in sfsz(mgindex) and shayao[u"陀罗"] in sfsz(mgindex) and huayao[u"化忌"][0] in sfsz(mgindex):
            result.append (u"贪狼落陷见羊陀又化忌，主面有疤痕，或有斑痣")
        if mgindex == fuyao[u"天马"]:
            result.append (u"贪狼天马善则擅长交际，恶则言语无实")
    if mgindex == zhengyao[u"巨门"]:
        result.append (u"巨门面型方长")
        if zhengyao[u"太阳"] in sfsz(mgindex) and ziweihelper.TYMX[zhengyao[u"太阳"]] == u"庙":
            result.append (u"巨门与入庙的太阳同度或会照，面色红黄")
        if zhengyao[u"太阳"] in sfsz(mgindex) and zhengyao[u"太阳"] in (5,6):
            result.append (u"巨门与巳午的太阳相会时，始主肥胖")
        if zhengyao[u"太阳"] in sfsz(mgindex):
            result.append (u"巨门会太阳，体毛多长")
    if mgindex == zhengyao[u"天相"]:
        result.append (u"天相面型方脸或微带圆，一般中等身材，中年后易转为肥胖")
        if gwzhi[6] in (zhengyao[u"廉贞"],zhengyao[u"破军"]):
            result.append (u"天相与廉贞破军相对，主暗破相")
    if mgindex == zhengyao[u"天梁"]:
        if mgindex == 6:
            result.append (u"天梁午宫主矮胖，眼光峻利逼人")
        if mgindex == 5:
            result.append (u"天梁巳宫则中年后始发胖，及主身长")
        if mgindex == zhengyao[u"天机"]:
            result.append (u"天梁与天机同度，擅长词令")
    if mgindex == zhengyao[u"七杀"]:
        result.append (u"七杀面型长方，带瘦者居多,化禄也可丰满")
    if mgindex == zhengyao[u"七杀"] and ziweihelper.QSMX[zhengyao[u"七杀"]] == u"陷" and shaji(mgindex,xingjis,3)==True:
        result.append (u"七杀落陷见刑忌,目露凶光")
    if mgindex == shayao[u"擎羊"]:
        result.append (u"女性相貌见擎羊才抢眼")
    if mgindex == shayao[u"陀罗"]:
        result.append (u"陀罗主牙齿不齐")
    if mgindex == zhengyao[u"破军"]:
        result.append (u"破军主人背厚眉宽，行坐腰斜,或破相，或口吃，或产时难产")
    return result


def ziwei_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    if mgindex == zhengyao[u"紫薇"]:
        if zhengyao[u"紫薇"]==6 and shayao[u"擎羊"]<>6 and shayao[u"陀罗"] <>6 and ygindex  in (0,3,5):
            result.append (u"紫微居午无刑忌，甲己丁人至公卿。")
        if (zhengyao[u"紫薇"] in (0,6) and huayao[u"化禄"][0] in sfsz(zhengyao[u"紫薇"]) and huayao[u"化权"][0] in sfsz(zhengyao[u"紫薇"]) and huayao[u"化科"][0] in sfsz(zhengyao[u"紫薇"])):
            result.append (u"紫微居子午，科禄权照最为奇。")
        if (sex == u"男" and zhengyao[u"紫薇"] ==11) or (sex == u"女" and zhengyao[u"紫薇"] ==2):
            result.append (u"紫微男亥女寅宫，壬甲生人富贵同。 此以得禄存同躔为富贵。")
        if zhengyao[u"紫薇"] in (3,9) and (kongyao[u"地劫"] == zhengyao[u"紫薇"] or kongyao[u"地空"] == zhengyao[u"紫薇"] or shayao[u"火星"] == zhengyao[u"紫薇"]
                                          or shayao[u"铃星"]== zhengyao[u"紫薇"] or shayao[u"擎羊"] == zhengyao[u"紫薇"] or shayao[u"陀罗"]== zhengyao[u"紫薇"]):
            result.append (u"紫微卯酉劫空煞，多为脱俗出家人。 （注）劫空指地劫地空，煞即四煞。")
    #紫微天府，全依辅弼之功。
    #（注）此言紫微或天府，非说紫府同宫。
    #紫府同宫无杀凑，甲人享福终身。（见图1例二）
    #（注）此亦以得禄存同躔为美。
    if (zhengyao[u"紫薇"] in (0,6) and mgindex == zhengyao[u"天相"] and mgindex == huayao[u"化禄"]) \
        or (zhengyao[u"紫薇"] in (1,7) and mgindex == zhengyao[u"天相"] and mgindex == huayao[u"化禄"]) \
        or (zhengyao[u"紫薇"] in (2,8) and mgindex == zhengyao[u"天相"] and mgindex == huayao[u"化禄"]) \
        or (zhengyao[u"紫薇"] in (4,10) and mgindex == zhengyao[u"廉贞"] and mgindex == huayao[u"化禄"]):
        result.append (u"紫府朝垣活禄逢，终身福厚至三公。 （注）活禄指化禄。此亦指紫府同宫。")
    #紫府同朝巳亥，一朝富贵双全。
    #（注）此指巳亥宫紫煞二星守命。（见图一例一
    if mgindex == zhengyao[u"紫薇"]:
        if zhengyao[u"紫薇"] in (0,6) and (huayao[u"化禄"] in sfsz(zhengyao[u"紫薇"]) or fuyao[u"禄存"] in sfsz(zhengyao[u"紫薇"])) and shayao[u"火星"] not in sfsz(zhengyao[u"紫薇"]) and \
           shayao[u"铃星"] not in sfsz(zhengyao[u"紫薇"]) and shayao[u"擎羊"] not  in sfsz(zhengyao[u"紫薇"]) and shayao[u"陀罗"] not in sfsz(zhengyao[u"紫薇"]):
            result.append (u"紫府日月居旺地，定出公侯器。 （注）紫居午，为日之旺地，府居子，为月之旰地。亦须无煞而见禄。")

    if (zhengyao[u"紫薇"] in sfsz(gwzhi[4]) and zhengyao[u"天府"] in sfsz(gwzhi[4]) and zhengyao[u"武曲"] in sfsz(gwzhi[4]) and huayao[u"化禄"][0] in sfsz(gwzhi[4]) and huayao[u"化权"][0] in sfsz(gwzhi[4])) \
        or (zhengyao[u"紫薇"] in sfsz(gwzhi[9]) and zhengyao[u"天府"] in sfsz(gwzhi[9]) and zhengyao[u"武曲"] in sfsz(gwzhi[9]) and huayao[u"化禄"][0] in sfsz(gwzhi[9]) and huayao[u"化权"][0] in sfsz(gwzhi[9])):
        result.append (u"紫府武曲临财宅，更兼权禄富奢翁。 （注）此言财帛宫或田宅宫。见此三正曜同会，得化权化禄。")
    if mgindex == zhengyao[u"紫薇"]:
        if zhengyao[u"紫薇"] in (1,7) and zhengyao[u"紫薇"] == fuyao[u"左辅"] and zhengyao[u"紫薇"] ==fuyao[u"右弼"]:
            result.append (u"紫微辅弼同宫，一呼百诺居上品的。 （注）此言紫微破军同在丑未。")
        if zhengyao[u"紫薇"] == shayao[u"擎羊"] and (huayao[u"化禄"][0] in sfsz(zhengyao[u"紫薇"]) or fuyao[u"禄存"] in sfsz(zhengyao[u"紫薇"])):
            result.append (u"紫府擎羊主巨商。 （注）亦必须见禄。迁移宫化禄尤佳。")
    if zhengyao[u"紫薇"] in (3,9) and mgindex == zhengyao[u"天机"]:
        result.append (u"紫府夹命为贵格。 （注）此言寅申二宫的天机太阴。")
    #紫禄同宫日月照，贵不可言。
    #（注）此言行经日月照之运限而骤贵。
    if mgindex == zhengyao[u"紫薇"]:
        if fuyao[u"文曲"] in sfsz(zhengyao[u"紫薇"]) and fuyao[u"文昌"] in sfsz(zhengyao[u"紫薇"]):
            result.append (u"紫微昌曲，富贵可期。 （注）此言得昌曲同躔或三方会照。")
        if zhengyao[u"紫薇"] in (5,11) and huayao[u"化权"][0] in sfsz(zhengyao[u"紫薇"]) and (huayao[u"化禄"][0] in sfsz(zhengyao[u"紫薇"]) or fuyao[u"禄存"] in sfsz(zhengyao[u"紫薇"])):
            result.append (u"紫微七杀，化权反作祯祥。 （注）须得禄，不须更得化权。")
    #紫破太阴煞曜逢，一生曹吏逞英雄。
    #（注）紫破守命见煞，至太阴运限为吏。
        if zhengyao[u"紫薇"] in (1,7) and fuyao[u"左辅"] not in sfsz(zhengyao[u"紫薇"]) and fuyao[u"右弼"] not in sfsz(zhengyao[u"紫薇"]) and fuyao[u"文曲"] not in sfsz(zhengyao[u"紫薇"]) \
                and fuyao[u"文昌"] not in sfsz(zhengyao[u"紫薇"]) and fuyao[u"天魁"] not in sfsz(zhengyao[u"紫薇"]) and fuyao[u"天钺"] not in sfsz(zhengyao[u"紫薇"]) \
                and fuyao[u"禄存"] not in sfsz(zhengyao[u"紫薇"]) and fuyao[u"天马"] not in sfsz(zhengyao[u"紫薇"]):
            result.append (u"紫破无辅佐，凶恶胥吏之徒。 （注）此即无百官朝拱之意。（见卷一）")
        if zhengyao[u"紫薇"] in (1,7) and shayao[u"擎羊"] in sfsz(zhengyao[u"紫薇"]) and shayao[u"陀罗"] in sfsz(zhengyao[u"紫薇"]):
            result.append (u"紫武破军会羊陀，欺公祸乱 （注）此亦旨紫破守命。")
        if zhengyao[u"紫薇"] == huayao[u"化权"][0] and (shayao[u"擎羊"] in sfsz(zhengyao[u"紫薇"]) and shayao[u"陀罗"] in sfsz(zhengyao[u"紫薇"]) \
                                                or (zhengyao[u"武曲"] in sfsz(zhengyao[u"紫薇"]) and zhengyao[u"武曲"]==huayao[u"化忌"][0])) :
            result.append (u"紫微权忌会羊陀，虽获吉而无道。 （注）此指紫微化权，会武曲比忌。")
    #紫微贪狼为至淫。
    #（注）此指泛水桃花之格（见卷一图44），亦指卯酉紫贪。（见卷一图22）
    #紫微于辰戌丑未加吉曜，富贵堪期。
    #(注)紫微忌四墓。尤忌辰戍罗网，此言加吉亦堪于中年后发福。
    #紫相辰戌，君臣不义。（见卷二）
    #（注）主反叛。
        if zhengyao[u"紫薇"] == fuyao[u"禄存"]:
            result.append (u"紫微禄存同宫，贵不可言。 （注）在命宫始是。凡紫微以得禄为贵。")
    #紫微诸煞同宫合诸吉，是为小人在位、君子在野，主人奸诈伪善。
    #（注）若吉煞同躔则不是。
    #女命紫微在子酉及巳亥，美玉瑕玷。
    #（注）在子为桃花；在酉为紫贪；在巳亥为紫杀。加煞即不佳。
    return result

def tianji_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '''
    天机寅命
    机梁会合善谈兵。
    （注）原注：居戌亦为美论。故此局乃指辰宫机梁而言。
    机梁守命加吉曜，富贵慈祥。
    （注）原注：加刑忌僧道。
    '''
    if mgindex == zhengyao[u"天机"] and mgindex in (4,10)  and sgindex == zhengyao[u"天同"]:
        result.append (u"机梁同照命身空，偏宜僧道。 （注）机梁守命，天同守身。（见图4）")
    # 机梁七杀破军冲，羽客僧流命所逢。
    #（注）机梁守命．行至匕杀破军运。主出家。然见煞空始是。
    if mgindex == zhengyao[u"天同"] and mgindex in (2,8):
        result.append(u"机月同梁作吏人。（注）同梁坐命，会机月.")
    if mgindex == zhengyao[u"天机"] and (huayao[u"化忌"][0] == zhengyao[u"天机"] or shayao[u"火星"] == zhengyao[u"天机"] or shayao[u"铃星"] == zhengyao[u"天机"] or shayao[u"擎羊"] == zhengyao[u"天机"] or shayao[u"陀罗"] == zhengyao[u"天机"]):
        result.append (u"天机加恶煞同宫，狗偷鼠窃。 （注）天机与刑忌煞空耗诸曜同宫。本句应读为「天机加恶、煞同宫」。")
    #天机巳宫卯酉逢，好饮离宗奸狡重。
    #（注）指巳卯酉三宫天机。见凶始是。
    if mgindex == zhengyao[u"天机"] and zhengyao[u"天机"] in (3,9):
        result.append (u"巨陷天机为破格。 （注）此指天机巨门在卯酉二宫安命而言，女命尤忌。男邪女淫。")
    '''天机卯酉，必退祖而自兴。（贝卷二）
    （注）见禄始是，见煞忌可参前注。
    机梁贪月同机会，暮夜经商无眼睡。
    （注）已见《太微赋》注（即卷一）。另一说，凡机粱、贪狼、太阴坐命者，行至天同、天机运，如所说。
    机梁同辰戊，必有高艺随身。（见图5）
    （注）借星安宫者不是，且须吉煞互见。
    机巨酉上化吉曜，纵遇财宫也不荣。
    （注）丑宫太阳未有光辉，但究胜于未宫太阳门落西山。卯宫「机巨」因借会丑宫太阳之故，便较酉宫「机巨」为优。（另注见卷二）
    机梁同在辰戌宫，加吉曜富贵慈祥。
    （注）见煞忌则偏宜僧道。但亦慈祥。
    '''
    return result

def taiyang_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '太阳'
    if mgindex == zhengyao[u"太阳"]:
        if zhengyao[u"太阳"] ==3 and (huayao[u"化禄"][0] in sfsz(zhengyao[u"太阳"]) or fuyao[u"禄存"] in sfsz(zhengyao[u"太阳"])):
            result.append (u"日照雷门，画生人富贵声扬。 （注）太阳在卯，为日照雷门。见禄始是。")
        if zhengyao[u"太阳"] ==6 and (huayao[u"化禄"][0] in sfsz(zhengyao[u"太阳"]) or fuyao[u"禄存"] in sfsz(zhengyao[u"太阳"])) and ygindex  in (3,5,6,7):
            result.append (u"太阳居午，庚辛丁己人富贵双全。 （注）此以得禄存或化禄为是。")
        #太阳文昌日在官禄，皇殿朝班。（见卷一）
        #（注）太阳必须庙旺。文曲同稍逊。
        if zhengyao[u"太阳"] in (3,9) and fuyao[u"文昌"]==zhengyao[u"太阳"] and zhengyao[u"太阳"] in (huayao[u"化禄"][0],fuyao[u"禄存"]):
            result.append (u"太阳天梁昌禄会，传胪第一名。 （注）此言太阳天梁在卯酉同度，会昌禄。")
        if zhengyao[u"太阳"] == huayao[u"化忌"][0] and (zayao[u"天刑"] in sfsz(zhengyao[u"太阳"]) or shayao[u"火星"] in sfsz(zhengyao[u"太阳"]) or shayao[u"铃星"] in sfsz(zhengyao[u"太阳"]) or shayao[u"擎羊"] in sfsz(zhengyao[u"太阳"]) or shayao[u"陀罗"] in sfsz(zhengyao[u"太阳"])):
            result.append (u"太阳化忌，是非日有目还伤。 （注）尤忌有煞同会。又忌见天刑。")
        if zhengyao[u"太阳"] == 8:
            result.append (u"日落未申在命位，为人先勤后惰。 （注）在申宫始是，主虎头蛇尾。")
        if zhengyao[u"太阳"] == 9:
            result.append (u"太阳酉宫守命，贵而不显，苗而不秀 （注）在酉宫为日落西山，故然。")
        if zhengyao[u"太阳"] in (10,11,0) and ((zhengyao[u"巨门"] in sfsz(zhengyao[u"太阳"]) and  huayao[u"化忌"][1] == u"巨门") or huayao[u"化忌"][1] == u"太阳"):
            result.append (u"太阳戌亥子，一生是非劳碌目还伤。 （注）巨门化忌劳禄是非，太阳化忌则主伤目。（见图6）")
    if zhengyao[u"太阳"] == 5 and zhengyao[u"巨门"] == 11 and mgindex == zhengyao[u"巨门"]:
        result.append (u"日巨拱照亦为奇。 （注）此即日在巳，巨在亥。巨门守命。")
    if mgindex == zhengyao[u"太阳"]:
        if zhengyao[u"太阳"] == zhengyao[u"巨门"] and zhengyao[u"太阳"] == 2 and huayao[u"化禄"][0] in sfsz(zhengyao[u"太阳"]) and huayao[u"化权"][0] in sfsz(zhengyao[u"太阳"]) and huayao[u"化科"][0] in sfsz(zhengyao[u"太阳"]):
            result.append (u"日巨同宫，官封三代。 （注）寅宫始是，须见禄权科。")
    if zhengyao[u"太阳"] == gwzhi[2] and fuyao[u"文曲"] in sfsz(zhengyao[u"太阳"]) and fuyao[u"文昌"] in  sfsz(zhengyao[u"太阳"]) and ziweihelper.TYMX[zhengyao[u"太阳"]] in (u"庙",u"旺"):
        result.append (u"日守夫妻诸吉聚，因妻得贵。 （注）须见昌曲，且须庙旺。")
    if zhengyao[u"太阳"] == gwzhi[2] and ziweihelper.TYMX[zhengyao[u"太阳"]] in (u"陷"):
        result.append (u"日守夫妻居陷地，加热伤妻。 （注）不需化忌已是。")
    if zhengyao[u"太阳"] in (gwzhi[4],gwzhi[9]) and ziweihelper.TYMX[zhengyao[u"太阳"]] in (u"庙",u"旺") and zhengyao[u"太阳"] not in (kongyao[u"地劫"],kongyao[u"地空"],shayao[u"火星"],shayao[u"铃星"]):
        result.append (u"太阳旺宫财宅位，若无空煞主积财。 （注）最忌空劫，火铃次之。又，田宅宫见之，主得尊长之荫。")
    if zhengyao[u"太阳"] == 6:
        result.append (u"太阳居迁移，难招祖业主离家。 （注）若陷地，离家亦不发。")
    if mgindex == zhengyao[u"太阳"] and sex == u"女" and ziweihelper.TYMX[zhengyao[u"太阳"]] in (u"庙",u"旺"):
        result.append (u"女命端正太阳星，早配贤夫信可凭。 （见卷二）（注）须在庙旺。")
    #日巳月酉，丑宫命步蟾宫。
    #（注）此局丑宫天粱安命，故仅主清贵。
    #日卯月亥，未宫命多折桂。（见图7）
    #（注）此局未宫无正曜，得禄权科，反为奇格。
    #日月同未命安丑，侯伯之材。（见卷二）
    #（注）此同丑宫无正曜，日月同在余宫来照，反较未宫见日月齐临者为佳。
    #日月命身居丑未，三方无吉反为凶。
    #（注）日月齐临必须见吉曜，无即破格。
    '''
    日月守命，不如照合并明。（见卷一）
    （注）此即综合前两句而言。
    日辰月戌并争辉，权禄非浅。（见图8）
    （注）须无煞忌，喜见昌曲。
    日月夹命夹财加吉曜，不权则富。
    （注）前论日月夹之格局中已说。（见卷一）
    日月最嫌反背。
    （注）日子月午、日戍月辰、日亥月巳，是为反背。
    阴阳左右合为佳。
    （注）以日与左辅同躔，月与右弼同躔，最为正格。日右月左次之。
    日月羊陀多克亲。
    （注）庙旺则未必可。
    日月陷宫逢恶煞，劳碌奔波。（见图6）
    （注）若庙旺，又得吉化，主劳碌而富。
    日月更须贪煞会，男多奸盗女多淫。
    （注）贪指桃花诸曜，非指贪狼。
    '''
    if mgindex == zhengyao[u"太阳"] and zhengyao[u"太阳"] == zhengyao[u"太阴"] and zhengyao[u"太阳"] == 5 and (gwzhi[5] in (kongyao[u"地劫"],kongyao[u"地空"]) or mgindex in (kongyao[u"地劫"],kongyao[u"地空"])):
        result.append (u"日月疾厄命宫空，腰驼目瞽。 （注）此言在疾厄宫，或命宫，见空劫。")
    return result

def wuqu_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '武曲'
    #武曲庙垣，威名赫奕。（见卷一）
    #（注）武曲在辰戌丑未四墓位为庙垣。
    if mgindex == zhengyao[u"武曲"] and zhengyao[u"武曲"] in (2,8) and fuyao[u"文曲"] in sfsz(zhengyao[u"武曲"]) and  fuyao[u"文昌"] in sfsz(zhengyao[u"武曲"]):
        result.append (u"武曲相遇昌曲逢，聪明巧艺定无穷。 （注）此言寅申宫武曲天相，更会昌曲。")
    if zhengyao[u"武曲"] in (mgindex,sgindex) and zhengyao[u"武曲"] in (2,8,5,11) and fuyao[u"禄存"] in sfsz(zhengyao[u"武曲"]) and fuyao[u"天马"] in sfsz(zhengyao[u"武曲"]):
        result.append (u"武曲禄马交驰，发财远郡。 （见图9）（注）寅申[武相]。或巳亥「武破」守命身，遇禄存、天马。大运遇之亦是，唯不若命身宫佳。")
    if mgindex == zhengyao[u"武曲"] and zhengyao[u"武曲"] in (1,7) and fuyao[u"天魁"] == zhengyao[u"武曲"] and fuyao[u"天钺"]== zhengyao[u"武曲"] and ziweihelper.WuQMX[zhengyao[u"武曲"]] in (u"庙",u"旺"):
        result.append (u"武曲魁钺居庙旺，财赋之官。 （注）以丑未宫「武贪」为佳。")
    if zhengyao[u"武曲"] == gwzhi[6]:
        result.append (u"武曲迁移，巨商高贾。 （见卷一图36）（注）寅申巳亥为行商，子午卯酉为坐贾。")
    if mgindex == zhengyao[u"武曲"]:
        if zhengyao[u"武曲"] in (3,9):
            result.append (u"武曲廉贞贪杀，便作经商。 （注）此言卯酉宫「武杀」。")
        if zhengyao[u"武曲"] in (1,7) and zhengyao[u"武曲"] in (shayao[u"擎羊"],shayao[u"陀罗"],kongyao[u"地劫"],kongyao[u"地空"]):
            result.append (u"武曲贪狼加煞忌，技艺之人。 （注）见火铃不是。煞指羊陀、空劫。")
    if zhengyao[u"武曲"] in (1,7) and zhengyao[u"武曲"] in (gwzhi[4],gwzhi[9]) and zhengyao[u"武曲"] in (shayao[u"火星"],shayao[u"铃星"]):
        result.append (u"武曲贪狼财宅位，横发资财 （注）须见火铃，为正火贪格。")
    if mgindex == zhengyao[u"武曲"]:
        if zhengyao[u"武曲"] in (5,11) and (huayao[u"化忌"][0] in sfsz(zhengyao[u"武曲"]) or shayao[u"火星"] in sfsz(zhengyao[u"武曲"]) or shayao[u"铃星"] in sfsz(zhengyao[u"武曲"]) \
                                          or shayao[u"擎羊"] in sfsz(zhengyao[u"武曲"]) or shayao[u"陀罗"] in sfsz(zhengyao[u"武曲"])):
            result.append (u"武曲破军，破祖破家劳碌。 （注）见煞忌始是。")
        if zhengyao[u"武曲"] in (3,7) and (huayao[u"化忌"][0] in sfsz(zhengyao[u"武曲"]) or shayao[u"火星"] in sfsz(zhengyao[u"武曲"]) or shayao[u"铃星"] in sfsz(zhengyao[u"武曲"]) \
                                          or shayao[u"擎羊"] in sfsz(zhengyao[u"武曲"]) or shayao[u"陀罗"] in sfsz(zhengyao[u"武曲"])):
            result.append (u"武曲破军会于卯地，木压雷惊。 （注）此言卯宫「武杀」会未宫「紫破」及亥宫「廉贪」，主有意外；或卯宫「廉破」会木宫「武贪」。二者均见见煞忌始应。其意外不限于所言。")
        if zhengyao[u"武曲"] in (0,6) and shayao[u"火星"] not in sfsz(zhengyao[u"武曲"]) and shayao[u"铃星"] not in sfsz(zhengyao[u"武曲"]):
            result.append (u"武曲天府同宫子午，主有寿。 （注）见火铃则不是。")
        if zhengyao[u"武曲"] in (3,9) and  shayao[u"火星"]==zhengyao[u"武曲"]:
            result.append (u"武曲七杀火星逢，因财被劫。 （注）指卯酉二宫。")
        if zhengyao[u"武曲"] in (3,9) and  zhengyao[u"武曲"] in (shayao[u"火星"],shayao[u"铃星"]) and shayao[u"擎羊"] in sfsz(zhengyao[u"武曲"]):
            result.append (u"武曲七杀会擎羊，因财持刀。 （见图10）（注）卯酉「武杀」，火铃同度，在三方会擎羊。")
        if zhengyao[u"武曲"] ==0 and (huayao[u"化忌"][0] in sfsz(zhengyao[u"武曲"]) or shayao[u"火星"] in sfsz(zhengyao[u"武曲"]) or shayao[u"铃星"] in sfsz(zhengyao[u"武曲"]) \
                                          or shayao[u"擎羊"] in sfsz(zhengyao[u"武曲"]) or shayao[u"陀罗"] in sfsz(zhengyao[u"武曲"])):
            result.append (u"武破贪狼居子位，投河溺水。 （注）子宫「武府」行至破贫相会之运限，原局煞忌，再见煞忌始应。")
        if zhengyao[u"武曲"] == kongyao[u"地劫"] and zhengyao[u"武曲"] == shayao[u"铃星"] and shayao[u"擎羊"] in sfsz(zhengyao[u"武曲"]):
            result.append (u"武曲劫煞会擎羊，因财持刀。 （注）劫指地劫，煞指火铃，以铃星为重。")
        if zhengyao[u"武曲"] == shayao[u"火星"] and zhengyao[u"武曲"] == shayao[u"陀罗"]:
            result.append (u"武曲羊陀兼火宿，丧命因财。 （注）以火星陀罗同宫为重。")
        #武曲之星为寡宿。（见卷二 （注）此论女命。
    return result

def tiantong_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '天同'
    if mgindex == zhengyao[u"天同"]:
        if fuyao[u"禄存"]  in sfsz(zhengyao[u"天同"]):
            result.append (u"天同会吉寿元长。  （见图11）（注）以会禄存为最佳，会昌曲则未必。")
        if zhengyao[u"天同"] == 6 and 6 in (shayao[u"擎羊"],shayao[u"陀罗"]) and ygindex  in (2,4):
            result.append (u"天同羊陀居午位，丙戌人镇御边疆。 （注）此即「马头带剑格」。（见卷图30）")
        if zhengyao[u"天同"] in (0,6) and huayao[u"化忌"][0] in sfsz(zhengyao[u"天同"]):
            result.append (u"同月陷宫加煞重，技艺、赢黄。 （注）「同阴」煞重即主为工匠且多病。午宫落陷固然，子宫亦有此倾向，见忌更的。")
        if zhengyao[u"天同"] ==10 and ygindex ==3 and huayao[u"化忌"][0] == 4:
            result.append (u"天同戌宫化忌，丁人命遇反为佳。 （注）此误。天同在戌，丁年人巨门在辰宫化忌，始为「反背」格局。（见卷二）")
        if zhengyao[u"天同"] in (1,7):
            result.append (u"天同巨门，即多感情困扰  女命天同必是贤。（注）此论未确。如天同巨门，即多感情困扰。且若天同巳亥宫化吉，女命虽美而淫。")
    return result

def lianzheng_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    if mgindex == zhengyao[u"廉贞"]:
        if zhengyao[u"廉贞"] in (7,8) and  shayao[u"火星"] not in sfsz(zhengyao[u"廉贞"]) and \
           shayao[u"铃星"] not in sfsz(zhengyao[u"廉贞"]) and shayao[u"擎羊"] not  in sfsz(zhengyao[u"廉贞"]) and shayao[u"陀罗"] not in sfsz(zhengyao[u"廉贞"]) and huayao[u"化忌"][0] not in sfsz(zhengyao[u"廉贞"]):
            result.append (u"廉贞申未宫无煞，富贵声扬播远名。 （注）此为廉贞制七杀，见《骨髓赋》注。（即卷二）")
        if zhengyao[u"廉贞"] in (3,9) and (shayao[u"火星"]  in sfsz(zhengyao[u"廉贞"]) or \
           shayao[u"铃星"]  in sfsz(zhengyao[u"廉贞"]) or shayao[u"擎羊"]   in sfsz(zhengyao[u"廉贞"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"廉贞"]) or  huayao[u"化忌"][0] in sfsz(zhengyao[u"廉贞"])):
            result.append (u"廉贞卯酉宫加煞，公胥无面官人。 （见卷二）（注）此言[廉破]在卯酉，贪墨胥吏。")
        if zhengyao[u"廉贞"] in (5,11) and fuyao[u"文曲"] == gwzhi[6]:
            result.append (u"廉贞贪杀破军逢，文曲迁移作贝戎。 （见卷二） （注）此言巳亥宫[廉贪]。对宫文曲。「贝戎」即「贼」字。")
        if zhengyao[u"廉贞"] == 7:
            result.append (u"廉贞七杀居庙旺，反为积富之人。 （见卷二）（注）[廉贞七杀]于未宫为奇格，丑宫不是。")
        if zhengyao[u"廉贞"] in (3,9,1,7) and shayao[u"火星"] == zhengyao[u"廉贞"] and huayao[u"化忌"][0] in sfsz(zhengyao[u"廉贞"]):
            result.append (u"廉贞破火居陷地，自缢投河。  （注）卯酉「廉破」，火星同度，又见忌。或丑未「廉杀」会破军，亦是。")
        if zhengyao[u"廉贞"] in (5,11):
            result.append (u"廉贞贪狼居巳亥，流荡天涯。 （注）参前「贪狼廉贞同度」条。（即卷二）")
        if zhengyao[u"廉贞"] ==8:
            result.append (u"廉贞入庙会将军，仲由威勐。 （见图12）（注）仅指廉贞独守申宫。仲由为孔门七十二贤之一，贤而能文复威勐。（见卷二）")
        #廉贞四煞遭刑戮。
        #（注）化忌，或见武曲化忌始是。
        if taisui12[u"白虎"] == zhengyao[u"廉贞"]:
            result.append (u"廉贞白虎，刑杖难逃。 （注）原局廉虎同宫，流年白虎又到，且见流煞。")
    if zhengyao[u"廉贞"] in sfsz(gwzhi[6]) and zhengyao[u"破军"] in sfsz(gwzhi[6]) and zhengyao[u"七杀"] in sfsz(gwzhi[6]) and (shayao[u"火星"]  in sfsz(gwzhi[6]) or \
           shayao[u"铃星"]  in sfsz(gwzhi[6]) or shayao[u"擎羊"]   in sfsz(gwzhi[6]) or shayao[u"陀罗"]  in sfsz(gwzhi[6]) or  huayao[u"化忌"][0] in sfsz(gwzhi[6])):
        result.append (u"廉贞破杀会迁移，死于外道。 （见卷一）（注）迁移宫见廉破杀，且见煞忌。")
    if zhengyao[u"廉贞"] in sfsz(gwzhi[8]) and zhengyao[u"廉贞"] == shayao[u"擎羊"]:
        result.append (u"廉贞羊煞居官禄，枷杒难逃。 （见卷一）（注）官禄宫见廉贞擎羊，流煞忌冲起。")
    #廉贞清白能相守。（见卷二）
    #（注）此言女命。有禄热煞，即是清白。
    if mgindex == zhengyao[u"廉贞"]:
        if zhengyao[u"廉贞"] == fuyao[u"文昌"] and  shayao[u"火星"] not in sfsz(zhengyao[u"廉贞"]) and \
           shayao[u"铃星"] not in sfsz(zhengyao[u"廉贞"]) and shayao[u"擎羊"] not  in sfsz(zhengyao[u"廉贞"]) and shayao[u"陀罗"] not in sfsz(zhengyao[u"廉贞"]) and huayao[u"化忌"][0] not in sfsz(zhengyao[u"廉贞"]):
            result.append (u"廉贞同文昌，好礼乐。 （注）无煞忌始是。")
        if zhengyao[u"廉贞"] == huayao[u"化禄"]:
            result.append (u"廉贞躔禄主富贵。 （见卷二图50）（注）若廉贞化禄见禄年，尤佳。")
        #廉贞遇羊陀，脓血不免。
        #（注）廉贞化忌为血光之灾。
        if zhengyao[u"武曲"]  in sfsz(zhengyao[u"廉贞"]) and zhengyao[u"破军"]  in sfsz(zhengyao[u"廉贞"]) and huayao[u"化忌"][1] == u"武曲":
            result.append (u"廉贞逢武破，砠业必破。 （见图13）（注）以武曲化忌为是。")
    return result

def tianfu_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '天府'
    if mgindex == zhengyao[u"天府"]:
        if zhengyao[u"天府"] ==10 and ygindex  in (0,5) and (huayao[u"化禄"][0] in sfsz(zhengyao[u"天府"]) or fuyao[u"禄存"] in sfsz(zhengyao[u"天府"])):
            result.append (u"天府戌宫无煞凑，甲己人腰金又且富。   #（见卷二） （注）天府必须得禄。")
        if zhengyao[u"天府"] in (6,10)  and zhengyao[u"天相"] in sfsz(zhengyao[u"天府"]) and fuyao[u"禄存"] in sfsz(zhengyao[u"天府"]) and  huayao[u"化禄"][0] in sfsz(zhengyao[u"天府"]) and  huayao[u"化权"][0] in sfsz(zhengyao[u"天相"]):
            result.append (u"天府居午戌，天相来朝一品贵。 （见图14）（注）必须天府得禄，天相得权。")
        if fuyao[u"禄存"] in sfsz(zhengyao[u"天府"]):
            result.append (u"天府天相天禄同，君臣庆会。 （注）此以天府为君，天相为臣。天禄指禄存。")
        if zhengyao[u"天府"] == zayao[u"天姚"] and fuyao[u"禄存"] not in sfsz(zhengyao[u"天府"]) and huayao[u"化禄"][0] not in sfsz(zhengyao[u"天府"]) and huayao[u"化科"][0] not in sfsz(zhengyao[u"天府"]):
            result.append (u"天府天姚多奸险。 （注）无禄始是。化科亦可解。")
        if fuyao[u"禄存"]  in sfsz(zhengyao[u"天府"]) and fuyao[u"文曲"] in sfsz(zhengyao[u"天府"]) and fuyao[u"文昌"] in sfsz(zhengyao[u"天府"]):
            result.append (u"天府禄存加昌曲，巨万之资。 （注）天府吉者，富乡于贵。紫微吉者，贵多于富。")
        if xiangjia(zhengyao[u"天府"],fuyao[u"文曲"],fuyao[u"文昌"]) or xiangjia(zhengyao[u"天府"],fuyao[u"天魁"],fuyao[u"天钺"]):
            result.append (u"天府昌曲左右，高第恩荣。 （注）昌曲魁钺亦是。")
    if zhengyao[u"天府"] == zhengyao[u"武曲"] and zhengyao[u"天府"] in (4,9) and (huayao[u"化禄"][0] in sfsz(mgindex) or huayao[u"化科"][0] in sfsz(mgindex)):
        result.append (u"天府武曲居财宅，更兼科禄富奢翁． （注）财宅指财帛、田宅二宫。")
    if mgindex == zhengyao[u"天府"]:
        if zhengyao[u"天府"] ==10 and zhengyao[u"天府"] == fuyao[u"左辅"]:
            result.append (u"左府同宫，尊居万乘。 （见卷二图54）（注）在戌宫安命始是。")
        if (shayao[u"火星"]  in sfsz(zhengyao[u"天府"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"天府"]) or shayao[u"擎羊"]  in sfsz(zhengyao[u"天府"]) \
                    or shayao[u"陀罗"]  in sfsz(zhengyao[u"天府"])) and  fuyao[u"禄存"] not in sfsz(zhengyao[u"天府"]):
            result.append (u"天府守命会四煞，为人奸诈。 （注）此为府库空露，无禄更劣。")
        if kongyao[u"地劫"] in sfsz(zhengyao[u"天府"]) or kongyao[u"地空"] in sfsz(zhengyao[u"天府"]) or kongyao[u"天空"] in sfsz(zhengyao[u"天府"]) \
            or zayao[u"正空"] in sfsz(zhengyao[u"天府"]):
            result.append (u"天府守命忌空亡。 （注）指空劫、正截空及天空。主孤立。")
    if mgindex not in (zhengyao) and mgindex in (5,11):
        result.append (u"府相同来会命宫，千锺食禄。 （见图15）（注）此指命在巳亥无正曜，府相来朝。")
    return result

def taiying_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '太阴'
    if mgindex == zhengyao[u"太阴"] and ygindex  in (2,3):
        result.append (u"太阴居子，丙丁富贵忠良。 （见卷一第73页）（注）画生人不是。")
    if zhengyao[u"太阴"] == fuyao[u"文曲"] and zhengyao[u"太阴"] == gwzhi[2]:
        result.append (u"太阴同文曲于妻宫，蟾宫折桂。 （见卷一第104页）（注）亦主聪明巧艺。")
#太阴武曲禄存同，左右相逢富贵翁。
#（注）夜生人太阴在命宫朝旺，行至武曲运限，见禄存主发。左右不过助力。
    if mgindex == zhengyao[u"太阴"]:
        if (shayao[u"擎羊"]  in sfsz(zhengyao[u"太阴"]) and shayao[u"铃星"]  in sfsz(zhengyao[u"太阴"])) or \
           (shayao[u"火星"]  in sfsz(zhengyao[u"太阴"]) and shayao[u"陀罗"]  in sfsz(zhengyao[u"太阴"])):
            result.append (u"太阴羊陀，必主人离财散。 （注）单见羊陀不是，须见羊铃，或见火陀始的。")
        if hzindex in (8,9,10,11,0,2) and zhengyao[u"太阴"] in (11):
            result.append (u"月朗天门于亥地，登云职掌大权。 （注）夜生人太阴在亥，为命宫，更见吉化及禄等。（见卷二第89页）")
            '''
            月曜天梁女淫贫。
            （注）太阴落陷，日生人，居巳宫，又见煞，或福德宫见煞，则不佳。（另注见卷二第204页）
            太阴落陷，夜生人伤母刑妻。
            （注）夜生人以太阴为主星，故不宜。
            '''
        if ziweihelper.TYiMX[zhengyao[u"太阴"]] in (u"陷") and huayao[u"化忌"][0] == zhengyao[u"太阴"] and hzindex in (2,3,4,5,6,7):
            result.append (u"太阴落陷且化忌，日生人随娘过继。 （注）太阴化忌日生人伤父。")
        if ziweihelper.TYiMX[zhengyao[u"太阴"]] in (u"陷") and ((shayao[u"擎羊"]  in sfsz(zhengyao[u"太阴"]) and shayao[u"铃星"]  in sfsz(zhengyao[u"太阴"])) \
           or (shayao[u"火星"]  in sfsz(zhengyao[u"太阴"]) and shayao[u"陀罗"]  in sfsz(zhengyao[u"太阴"]))):
            result.append (u"太阴落陷遇羊陀，肢体伤残。 （注）见羊铃或火陀始的。")
        if zhengyao[u"太阴"] in (2) and fuyao[u"文曲"] == zhengyao[u"太阴"] and fuyao[u"文昌"] == zhengyao[u"太阴"] and (shayao[u"火星"] in sfsz(zhengyao[u"太阴"]) or \
           shayao[u"铃星"]  in sfsz(zhengyao[u"太阴"]) or shayao[u"擎羊"]   in sfsz(zhengyao[u"太阴"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"太阴"]) or huayao[u"化忌"][0]  in sfsz(zhengyao[u"太阴"])):
            result.append (u"太阴天机同昌曲，男为奴仆女为娼。 （注）寅宫始是，申宫者不然，且须化忌及见煞耗。")
        #太阴文曲，定是九流术士。
        #（注）文曲主偏才。故然。阴阳家于九流十家中居九，故曰九流术士。
    if zhengyao[u"太阴"] == gwzhi[5] and shayao[u"陀罗"] == gwzhi[5] and shayao[u"火星"] in sfsz(zhengyao[u"太阴"]) and shayao[u"铃星"] in sfsz(zhengyao[u"太阴"]):
        result.append (u"太阴疾厄遇陀罗，火铃目疾为灾。 （见图16）（注）太阴疾厄遇陀罗同度，会火铃。")
    return result

def tanlang_rule(sex,ygindex,yzindex,hzindex,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '贪狼'
    if mgindex == zhengyao[u"贪狼"]:
        if zhengyao[u"贪狼"] in (4,10,1,7) and shayao[u"火星"] in (gwzhi[0],gwzhi[6]) and shayao[u"铃星"] in (gwzhi[0],gwzhi[6]) :
            result.append (u"贪狼铃火四墓宫。豪富家资侯伯贵。 （见卷二第61页）（注）四墓即辰戌丑未。铃火以与贪狼同躔为佳。在对宫者较次。")
        if zhengyao[u"贪狼"] in (4,10,1,7):
            result.append (u"贪狼入庙寿元长。 （注）指辰戌丑未四宫贪狼，丑未为次。")
        #贪狼会煞无吉曜，屠宰之人。（见图17）（注）『廉贪』见煞为最。化忌尤确。
        if zhengyao[u"贪狼"] in (0,6,3,9):
            result.append (u"贪狼子午卯酉，鼠窃狗偷之辈，终身不能有为。 （注）此已于《大微赋》注中详说。（见卷一第113页）")
        if zhengyao[u"贪狼"] in (fuyao[u"左辅"],fuyao[u"右弼"],fuyao[u"天魁"],fuyao[u"天钺"]) and zhengyao[u"贪狼"] == changsheng12[0]:
            result.append (u"贪狼加吉坐长生，寿考永如彭祖。 （见卷一第120页）（注）加吉指魁铍、辅弼。若昌曲不是。")
        if zhengyao[u"贪狼"] in (5,11) and (shayao[u"火星"] in sfsz(zhengyao[u"贪狼"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"贪狼"]) \
           or shayao[u"擎羊"]   in sfsz(zhengyao[u"贪狼"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"贪狼"]) or huayao[u"化忌"][0]  in sfsz(zhengyao[u"贪狼"])):
            result.append (u"贪狼巳亥加煞，不为屠户便遭刑。 （见图17）（注）为屠户亦主短命。")
        if zhengyao[u"贪狼"] == zhengyao[u"武曲"]:
            result.append (u"贪武先贫而后富。  贪狼武曲同行，晚景边夷神服。（注）此言中年后始发。运限须见吉化。贪武先贫而后富。（见卷二第30页及163页）（注）运限逢禄始是。")
        if zhengyao[u"贪狼"] == fuyao[u"文昌"] and zhengyao[u"贪狼"] == fuyao[u"文曲"] and huayao[u"化科"][0] not in (fuyao[u"文昌"],fuyao[u"文曲"]):
            result.append (u"贪狼昌曲同宫，多虚少实。（注）除非昌曲化科。")
        if zhengyao[u"贪狼"] ==8  and zhengyao[u"廉贞"] == gwzhi[6] and huayao[u"化忌"][1] == u"廉贞":
            result.append (u"贪狼申宫为下格。 （注）见对宫廉贞化忌始是。")
        #贪狼忌煞同乡，女伦期而男鼠窃。（注）此指在四旺宫，参见《太微赋》注（卷一第113页）。
        if zhengyao[u"贪狼"] in (4,10,1,7) and zhengyao[u"破军"] in sfsz(zhengyao[u"贪狼"]) and huayao[u"化忌"][1] == u"破军" and (shayao[u"火星"] in sfsz(zhengyao[u"贪狼"]) or \
           shayao[u"铃星"]  in sfsz(zhengyao[u"贪狼"]) or shayao[u"擎羊"]   in sfsz(zhengyao[u"贪狼"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"贪狼"])):
            result.append (u"贪狼四生四墓宫。破军忌煞百工通。 （注）此言会破军及化忌、四煞。")
    if sgindex == zhengyao[u"贪狼"] and sgindex == zhengyao[u"武曲"] and (shayao[u"擎羊"]   in sfsz(zhengyao[u"贪狼"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"贪狼"])) \
            and fuyao[u"左辅"] not in sfsz(zhengyao[u"贪狼"]) and fuyao[u"右弼"] not in sfsz(zhengyao[u"贪狼"]) and fuyao[u"文曲"] not in sfsz(zhengyao[u"贪狼"]) \
            and fuyao[u"文昌"] not in sfsz(zhengyao[u"贪狼"]) and fuyao[u"天魁"] not in sfsz(zhengyao[u"贪狼"]) and fuyao[u"天钺"] not in sfsz(zhengyao[u"贪狼"]):
        result.append (u"贪狼武曲同守身命，无吉命反不长。 （注）此指无吉复见羊陀。")
    if mgindex == zhengyao[u"贪狼"]:
        if zhengyao[u"武曲"] in sfsz(zhengyao[u"贪狼"]) and zhengyao[u"破军"] in sfsz(zhengyao[u"贪狼"]) and (zayao[u"红鸾"] in sfsz(zhengyao[u"贪狼"]) \
            or zayao[u"天喜"] in sfsz(zhengyao[u"贪狼"]) or zayao[u"天姚"] in sfsz(zhengyao[u"贪狼"]) or zayao[u"咸池"] in sfsz(zhengyao[u"贪狼"]) \
            or zayao[u"大耗"] in sfsz(zhengyao[u"贪狼"]) or changsheng12[0] in sfsz(zhengyao[u"贪狼"])):
            result.append (u"贪武破军无吉曜，迷花恋酒以亡身。 （注）见桃花始是，见煞主手艺。")
        if zhengyao[u"太阴"] in sfsz(zhengyao[u"贪狼"]) and zhengyao[u"天机"] in sfsz(zhengyao[u"贪狼"]) and zhengyao[u"天梁"] in sfsz(zhengyao[u"贪狼"]) \
            and (shayao[u"火星"] in sfsz(zhengyao[u"贪狼"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"贪狼"]) \
            or shayao[u"擎羊"]   in sfsz(zhengyao[u"贪狼"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"贪狼"]) or huayao[u"化忌"][0]  in sfsz(zhengyao[u"贪狼"])):
            result.append (u"贪月同煞会机粱，贪财无厌作经商。  （注）参见天机之「机梁会月同机会」条。（第12页或见卷一第109页）")
        if zhengyao[u"贪狼"] == zhengyao[u"廉贞"] and (zayao[u"红鸾"] in sfsz(zhengyao[u"贪狼"]) \
            or zayao[u"天喜"] in sfsz(zhengyao[u"贪狼"]) or zayao[u"天姚"] in sfsz(zhengyao[u"贪狼"]) or zayao[u"咸池"] in sfsz(zhengyao[u"贪狼"]) \
            or zayao[u"大耗"] in sfsz(zhengyao[u"贪狼"]) or changsheng12[0] in sfsz(zhengyao[u"贪狼"])) \
            and (shayao[u"火星"] in sfsz(zhengyao[u"贪狼"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"贪狼"]) \
            or shayao[u"擎羊"]   in sfsz(zhengyao[u"贪狼"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"贪狼"]) or huayao[u"化忌"][0]  in sfsz(zhengyao[u"贪狼"])) \
            and fuyao[u"禄存"] not  in sfsz(zhengyao[u"贪狼"]) and (fuyao[u"天马"] in sfsz(zhengyao[u"贪狼"]) or shayao[u"火星"] in sfsz(zhengyao[u"贪狼"])):
            result.append (u"贪狼廉贞同度，男多浪荡女多淫。 （见图18）（注）见煞及桃花．又见天马无禄，或见火星无禄始是。")
        if zhengyao[u"贪狼"] in (11,0) and (shayao[u"擎羊"]   in sfsz(zhengyao[u"贪狼"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"贪狼"])):
            result.append (u"贪遇羊陀居亥子，名为泛水桃花。 （注）见《太微赋》注（即卷一第87页）。")
        if zhengyao[u"贪狼"] ==2 and shayao[u"陀罗"] == 2:
            result.append (u"贪狼陀罗在寅宫，号曰风流彩杖。 （注）见《大微赋》注（即卷一第87页）。")
        #女命贪狼多嫉妒。（注）遇羊陀始是。（见卷二第211页）
    return result

def jumen_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '巨门'
    if mgindex == zhengyao[u"巨门"]:
        if zhengyao[u"巨门"] == zhengyao[u"太阳"] and zhengyao[u"巨门"] in (2,8):
            result.append (u"巨日寅宫立命申，先驱名而食禄。巨日命宫寅位，贪禄驰名。 （见图19）（注）巨门太阳以同居寅宫为贵。若申宫安命借星，先名后利；若寅宫安命，则先利后名。")
        if zhengyao[u"巨门"] in (0,6) and huayao[u"化禄"][0]  in sfsz(zhengyao[u"巨门"]) and huayao[u"化权"][0]  in sfsz(zhengyao[u"巨门"]) and huayao[u"化科"][0]  in sfsz(zhengyao[u"巨门"]):
            result.append (u"巨门子午科权禄，石中隐玉福兴隆。 （注）详见「石中隐玉」格注。(见卷二第156页)")
        if zhengyao[u"巨门"] ==11:
            result.append (u"巨在亥宫日命巳，贪禄驰名。")
        if zhengyao[u"巨门"] in (5):
            result.append (u"巨在巳宫日命亥，反为不佳。 （注）太阳在巳则佳，在亥不妙。巨日拱照亦为奇。（注）此即巨在亥，日在巳，巨门守命。")
        if zhengyao[u"巨门"] in (3) and ygindex in (1,2,5,7) and (fuyao[u"禄存"]  in sfsz(zhengyao[u"巨门"]) or huayao[u"化禄"][0]  in sfsz(zhengyao[u"巨门"]) \
            and shayao[u"火星"] not in sfsz(zhengyao[u"巨门"]) and shayao[u"铃星"] not in sfsz(zhengyao[u"巨门"]) \
            and shayao[u"擎羊"]  not in sfsz(zhengyao[u"巨门"]) and shayao[u"陀罗"] not  in sfsz(zhengyao[u"巨门"]) and huayao[u"化忌"][0] not in sfsz(zhengyao[u"巨门"])):
            result.append (u"巨机居卯，乙辛己丙至公卿。 （注）此以得禄为佳，有煞同不是。")
        if zhengyao[u"巨门"] in (9):
            result.append (u"巨机酉上化吉者，纵有财官不善终。 （注）酉宫「机巨」。富不长寿，贫反延年。")
        if zhengyao[u"巨门"] in (4) and huayao[u"化忌"][1]==u"巨门" and huayao[u"化权"][1]==u"天同" and ygindex == 3:
            result.append (u"巨机辰宫化忌，辛人命遇反为奇。（注）此条误。应为巨门在辰化忌，对宫天同化权，成奇格。然此必丁年生人。")
    if  zhengyao[u"巨门"] in (shayao[u"擎羊"],shayao[u"陀罗"]) and  zhengyao[u"巨门"] in (mgindex,sgindex,gwzhi[5]) and huayao[u"化忌"][1]==u"巨门":
        result.append (u"巨门羊陀于身命疾厄，羸黄困弱盗而娼。（见卷一第123页）（注）此言命身宫或疾厄宫之应。唯巨门比忌始是。")
    if mgindex == zhengyao[u"巨门"]:
        if zhengyao[u"巨门"] in (1,7) and (shayao[u"火星"] in sfsz(zhengyao[u"巨门"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"巨门"]) \
            or shayao[u"擎羊"]   in sfsz(zhengyao[u"巨门"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"巨门"]) or huayao[u"化忌"][0]  in sfsz(zhengyao[u"巨门"])) :
            result.append (u"巨同丑未为下格。（注）丑未宫天同巨门见煞忌刑耗。") # 刑耗 ?
        if zhengyao[u"巨门"] == shayao[u"陀罗"] and shayao[u"火星"] in sfsz(zhengyao[u"巨门"]):
            result.append (u"巨门陀罗，必生异痣。（注）加会火星始是、亦主胎记 ")
#辰戌应嫌陷巨门。（注）此条详见《骨髓赋》注（即卷二第110页）。
#巨宿同梁冲且合，子羽才能。（见图20）（注）须申宫安命无正曜，对宫「日巨」、子宫「阴同」、辰宫「机梁」来会，且须丁年生人。得吉化始是。
        if (shayao[u"擎羊"]  in sfsz(zhengyao[u"巨门"]) and shayao[u"铃星"]  in sfsz(zhengyao[u"巨门"])) \
            or (shayao[u"陀罗"]  in sfsz(zhengyao[u"巨门"]) and shayao[u"火星"]  in sfsz(zhengyao[u"巨门"])):
            result.append (u"巨门守命，三合煞凑必遭火厄。（注）见羊铃或火陀始是。")
    if zhengyao[u"巨门"] == gwzhi[1] and huayao[u"化忌"][0]  in sfsz(zhengyao[u"巨门"]) and (shayao[u"火星"] in sfsz(zhengyao[u"巨门"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"巨门"]) \
            or shayao[u"擎羊"]   in sfsz(zhengyao[u"巨门"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"巨门"])):
        result.append (u"巨门守兄弟，骨肉参商。（见图21）（注）化忌见煞始是。若会太阴化忌，是非起于妯娌。")
    if zhengyao[u"巨门"] == gwzhi[3] and (shayao[u"火星"] in sfsz(zhengyao[u"巨门"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"巨门"]) \
            or shayao[u"擎羊"]  in sfsz(zhengyao[u"巨门"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"巨门"]) or huayao[u"化忌"][0] in sfsz(zhengyao[u"巨门"])):
        result.append (u"巨门子女，损后方招。（注）见煞忌始是。否则虽有如无。")
    if mgindex == zhengyao[u"巨门"]:
        if zhengyao[u"巨门"] in (4,10) and (shayao[u"火星"] in sfsz(zhengyao[u"巨门"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"巨门"]) \
            or shayao[u"擎羊"]  in sfsz(zhengyao[u"巨门"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"巨门"])):
            result.append (u"巨门四煞陷而凶。（注）巨门居辰戌为落陷。")
        #巨门擎火羊陀逢恶曜，防缢死投河。（见卷二第137页）（注）恶曜指化忌及刑耗。
        #巨火铃星，逢恶限死外道。（注）各宫巨门有不同的敏感外限，详见拙着《中州派紫微斗数》。
        if zhengyao[u"巨门"]  == zhengyao[u"天机"]  and huayao[u"化忌"][0] in sfsz(zhengyao[u"巨门"]) and (shayao[u"火星"] in sfsz(zhengyao[u"巨门"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"巨门"]) \
            or shayao[u"擎羊"]  in sfsz(zhengyao[u"巨门"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"巨门"])):
            result.append (u"巨宿天机为破荡。（见卷二第200页）（注）此指女命，化忌见煞始是。")
    return result

def tianxiang_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '天相'
    if mgindex == zhengyao[u"天相"]:
        if zhengyao[u"天相"] in (0,6) and fuyao[u"禄存"] == zhengyao[u"天相"] and xiangjia(zhengyao[u"天相"],shayao[u"擎羊"],shayao[u"陀罗"]):
            result.append (u"天相廉贞羊陀夹，多招刑杖祸难逃。（见图22）（注）此言子午宫廉相与禄存同度")
        if zhengyao[u"天相"]  ==  fuyao[u"右弼"]:
            result.append (u"天相右弼福来临。（见卷二第194页）（注）此主受人提拔而发福。亦宜女命。")
        #天相之星女命躔，必当子贵与夫贤。（注）此仅言能相夫教子，非必贵与贤也。
        if zhengyao[u"天相"] in (3,9) and (shayao[u"擎羊"]  in sfsz(zhengyao[u"天相"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"天相"])):
            result.append (u"天相陷地，贪廉武破羊陀凑，巧艺安身。(见图23)（注）此指天相居卯酉。")
        if (fuyao[u"文曲"] in sfsz(zhengyao[u"天相"]) and huayao[u"化忌"][1] == u"文曲") or  (fuyao[u"文昌"]  in sfsz(zhengyao[u"天相"])  and huayao[u"化忌"][1] == u"文昌") \
            or (shayao[u"火星"] in sfsz(zhengyao[u"巨门"]) and shayao[u"铃星"] in sfsz(zhengyao[u"巨门"])):
            result.append (u"天相昌曲，逢冲破主作偏房。（注）此指女命。不宜昌曲化忌，化忌即破：亦不宜见火铃冲会。")
        if zhengyao[u"天相"] in (0,6) and shayao[u"擎羊"]  in sfsz(zhengyao[u"天相"]) and ygindex in (2,8):
            result.append (u"天相廉贞守命见羊刑，刑杖难逃。（见图24）（注）子午宫「廉相」，丙人在午宫；壬人在子宫即是。丙人尤劣，以廉贞化忌故")
    return result

def tianliang_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '天梁'
    if mgindex == zhengyao[u"天梁"]:
        if zhengyao[u"天梁"] == 6 and zhengyao[u"天梁"] and huayao[u"化权"][0] in sfsz(zhengyao[u"天梁"]) and huayao[u"化科"][0] in sfsz(zhengyao[u"天梁"]):
            result.append (u"天梁居午位，官资清显。（见卷二第95页）（注）以得科权者始是。")
            #天梁守照吉星逢，平生福寿。（注）在午宫最佳，落陷不是。
        if zhengyao[u"天梁"] in (3,9) and fuyao[u"文昌"] in sfsz(zhengyao[u"天梁"]) and fuyao[u"禄存"] in sfsz(zhengyao[u"天梁"]):
            result.append (u"天梁太阳昌禄会，传胪第一名。（注）此言卯酉二宫。阳粱同度会昌禄。天粱文昌居庙旺，位至台纲。（注）除巳申亥酉四宫皆庙旺。台纲即御史。此言能得清贵，不主富。")
    if zhengyao[u"天梁"] == gwzhi[6]:
        result.append (u"天梁加吉坐迁移，巨商高实。（注）天梁守命不主富，守迁移却可富。（见卷一图64）")
    #天梁天马，为人飘荡风流。（见卷二图35）（注）巳申二宫较重，寅亥二宫较轻。
    if mgindex == zhengyao[u"天梁"]:
        if zhengyao[u"天梁"] == 9:
            result.append (u"梁宿太阴，却作飘蓬之客。（注）此指阳梁居酉，会太阴居巳。")
        if zhengyao[u"天梁"] in (5,11):
            result.append (u"梁同巳亥，男多浪荡女多淫。（见卷二第204页）（注）梁在巳，天同在寅对照。或梁在亥，天同在巳。前者较劣。")
        #天梁月曜女淫贫。（注）日生人，太阴居巳宫落陷见煞，或福德宫见煞，不佳。
        if zhengyao[u"天梁"] in (2,8):
            result.append (u"粱同机月寅申位，一生利业聪明。（见图25）（注）指寅申宫梁同会机月，主尖刻。")
        if shayao[u"陀罗"] in sfsz(zhengyao[u"天梁"]) and zhengyao[u"太阴"] in sfsz(zhengyao[u"天梁"]) and shayao[u"铃星"] in sfsz(zhengyao[u"天梁"]):
            result.append (u"梁陀阴铃，拟作栋梁之客。（注）四曜同会，为盗贼。或卑贱而贪。")
        if zhengyao[u"天梁"]  in (5,8,11) and (shayao[u"擎羊"] in sfsz(zhengyao[u"天梁"]) or shayao[u"陀罗"] in sfsz(zhengyao[u"天梁"])):
            result.append (u"天梁陷地见羊陀，伤风败俗。（注）天梁于巳申亥宫落陷。")
        if zhengyao[u"天梁"]  in (4,10):
            result.append (u"梁机同在辰戌宫，加吉曜富贵慈祥。（见第11页图4）（注）见煞忌则偏宜僧道，但亦慈祥。")
            result.append (u"梁机同辰戌，必有高艺随身。（见第13页图5）（注）借星安宫者不是。且须吉煞互见。")
    return result

def qisha_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '七杀'
    if mgindex == zhengyao[u"七杀"]:
        if zhengyao[u"七杀"] in (2,8,0,6):
            result.append (u"七杀寅申子午位，一生爵禄荣昌。（见图26）（注）子位不是。盖午得廉贞在申宫为福德，可以相制；寅申则为朝斗格，唯见吉化始的。")
    if zhengyao[u"七杀"] in (mgindex,sgindex) and huayao[u"化禄"][0] not in sfsz(zhengyao[u"七杀"]):
        result.append (u"七杀临身命，流年刑忌灾伤。（注）原局七坐命宫。流年又至七杀位，见刑忌流煞等凶曜（见卷一图82）会禄可解。")
    if mgindex == zhengyao[u"七杀"]:
        if zhengyao[u"七杀"]  == changsheng12[u"绝"] and (shayao[u"擎羊"] in sfsz(zhengyao[u"七杀"]) or shayao[u"陀罗"] in sfsz(zhengyao[u"七杀"])):
            result.append (u"杀临绝地会羊陀，颜回夭折。（注）原局七杀居于绝地，流年若再巡逢七段位；原局羊陀照会，被流羊流陀卫起。唯会禄可解。")
        if  huayao[u"化忌"][0] in sfsz(zhengyao[u"七杀"]) or (shayao[u"火星"] in sfsz(zhengyao[u"七杀"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"七杀"]) \
                or shayao[u"擎羊"]  in sfsz(zhengyao[u"七杀"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"七杀"])):
            result.append (u"七杀重逢四杀，腰驼背曲阵中亡。（注）原局七杀有煞，流年再逢七杀，复见流杀（煞），是年主意外兵伤。原局火铃同躔七杀者尤甚。")
        if shayao[u"铃星"] in sfsz(zhengyao[u"七杀"]) and shayao[u"擎羊"] in sfsz(zhengyao[u"七杀"]):
            result.append (u"七杀火羊贫且贱，屠宰之人。（注）误。铃羊同躔始是。")
        # 七杀羊铃，流年白虎刑戮灾遁。（见卷一图83及84）（注）原局七杀羊铃同躔。流年白虎行至，然仅主官司词讼，未至刑戮。七杀流羊二官符，离乡遭配。（注）七杀与官符安命，流年行至本宫，又见流年官符同度，且见流羊。原局行火铃者尤凶。
        if zhengyao[u"七杀"] in (5,11) and huayao[u"化权"][0] not in sfsz(zhengyao[u"七杀"]):
            result.append (u"七杀紫薇，化权反作祯祥。（注）须得禄，不须更得化权。")
        if zhengyao[u"七杀"] == shayao[u"擎羊"] and zhengyao[u"七杀"] == shayao[u"铃星"]:
            result.append (u"七杀破军，真依羊铃之虐。（见卷一第13页）（注）七杀与破军，与单铃同度，皆为不吉。此非专指七杀而言。")
        if zhengyao[u"七杀"] ==7:
            result.append (u"七杀廉贞居庙旺，反为积富之人。（见卷二第24页）（注）「七杀贞贞」于未宫为奇格，丑宫不是。")
        #七杀廉贞同位，路上埋尸。（注）见《太微赋》注内详（即卷一第212页）。七杀破军宜外出，诸般手艺不能精。（见图27）（注）七杀居陷地，或破军无禄皆有此应。七杀沉吟福不荣。（见卷二第212页）（注）此指女命。沉吟者，居巳亥陷地。
    if zhengyao[u"七杀"] == sgindex:
        result.append (u"七杀临身终是天。（注）此指身宫七杀，若大限流年之流身主见七杀、破军，是为「竹箩三限」。少年遇之主夭，或重病（详见卷四《零谈》。）")
    #七杀单居福德，女人切忌贱无疑。（注）此条武断。
    #七杀守照，岁限擎羊，午生人卯酉宫安命，主凶亡。（注）此即言「七杀重逢，羊陀迭并」。所学之例不合。
    return result

def pojun_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '破军'
    if mgindex == zhengyao[u"破军"]:
        if zhengyao[u"破军"] in (0,6) and (fuyao[u"禄存"] in sfsz(zhengyao[u"破军"]) or huayao[u"化禄"][0] in sfsz(zhengyao[u"破军"])) and shayao[u"火星"] not in sfsz(zhengyao[u"破军"]) \
                and shayao[u"铃星"] not in sfsz(zhengyao[u"破军"]) and shayao[u"擎羊"] not in sfsz(zhengyao[u"破军"]) and shayao[u"陀罗"] not in sfsz(zhengyao[u"破军"]):
            result.append (u"破军子午宫无杀，官资清显至三公。（注）必须得禄始是。")
        if fuyao[u"禄存"] in sfsz(zhengyao[u"破军"]) and fuyao[u"天马"] in sfsz(zhengyao[u"破军"]) and zhengyao[u"天府"] == zayao[u"天姚"] \
                and (shayao[u"火星"] not in sfsz(zhengyao[u"破军"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"破军"])):
            result.append (u"破军贪狼逢禄马，男多浪荡女多淫。（见图28）（注）破军会贪狼，逢禄马。以巳亥二宫为紧。然必见火铃及桃花诸曜者始应。若福德宫天府见天姚。尤验。")
        if zhengyao[u"破军"]  in (11,0,1) and zhengyao[u"破军"] == fuyao[u"文曲"] and (huayao[u"化忌"][1] == u"武曲" or huayao[u"化忌"][0] == zhengyao[u"破军"]):
            result.append (u"破军暗曜共乡，水中作冢。（注）破军文曲同躔于亥子丑三宫。见武曲化忌始是。文曲化忌亦不宜。子午宫则主在外乡有祸，以武曲化忌会迁移之故。（见卷一图49）")
        if zhengyao[u"破军"]  in (0,6) and huayao[u"化忌"][1] == u"武曲" :
            result.append (u"破军暗曜共乡，水中作冢。（注）破军文曲同躔于亥子丑三宫。见武曲化忌始是。文曲化忌亦不宜。子午宫则主在外乡有祸，以武曲化忌会迁移之故。（见卷一图49）")
        #破军火铃，奔波劳碌。（注）田宅宫见亦是。主屡屡迁家换宅。
        #破军一曜性难明。（见卷二第210页）（注）此言女命。谓其性不常。易喜易怒，忽憎忽爱。
    if zhengyao[u"破军"] in (3,9) and zhengyao[u"破军"] == gwzhi[8] and (shayao[u"擎羊"] not in sfsz(zhengyao[u"破军"]) or shayao[u"陀罗"] not in sfsz(zhengyao[u"破军"])):
        result.append (u"破耗羊铃官禄位，到处乞求。（注）指卯酉「廉破」为官禄宫。")
    if mgindex == zhengyao[u"破军"]:
        if zhengyao[u"破军"] in (0,6) and huayao[u"化忌"][1] == u"廉贞":
            result.append (u"破军子午，见煞忌孤单残疾。（注）不宜见廉贞化忌。见则不宜更见天马。")
        if zhengyao[u"破军"] in (4,10,1,7) and ygindex in (2,4):
            result.append (u"破军辰戌丑未宫，丙戊生人富贵同。（注）丙年生人，主得父荫，戊年生人则须自创。皆取化禄为用。古代女命皆主封赠。（见图29）")
    if zhengyao[u"破军"] == zhengyao[u"武曲"] and zhengyao[u"破军"] == gwzhi[4] and huayao[u"化忌"][1] == u"武曲":
        result.append (u"破军武曲入财乡。东倾西败。（注）武曲化忌始是。")
    if mgindex == zhengyao[u"破军"]:
        if fuyao[u"文昌"] in sfsz(zhengyao[u"破军"]) or fuyao[u"文曲"] in sfsz(zhengyao[u"破军"]) and huayao[u"化忌"][1] in (u"文昌",u"文曲"):
            result.append (u"破军昌曲逢，刑克多劳。（注）昌曲化忌始是。")
        if zhengyao[u"破军"] in (2) and fuyao[u"文昌"] in sfsz(zhengyao[u"破军"]) or fuyao[u"文曲"] in sfsz(zhengyao[u"破军"]) and huayao[u"化科"][1] in (u"文昌",u"文曲"):
            result.append (u"破军昌曲寅命宫，贵显至三公。（注）此指昌曲化科。")
        #破军昌曲，一生贫士。（注）昌曲化忌始的。
    if  zhengyao[u"破军"] in (mgindex , gwzhi[5]) and zhengyao[u"破军"] in (shayao[u"擎羊"],shayao[u"陀罗"]):
        result.append (u"破军羊陀，身命疾厄主残疾。（注）破军羊陀在命宫及疾厄宫为的。")
    if  zhengyao[u"破军"] == gwzhi[1] and zhengyao[u"破军"] in (shayao[u"火星"],shayao[u"铃星"]):
        result.append (u"破军居兄弟，骨肉参商。（注）不宜火铃同躔。")
    if  zhengyao[u"破军"] == gwzhi[4] and huayao[u"化禄"][0] not in sfsz(zhengyao[u"破军"]) and fuyao[u"禄存"] not in sfsz(zhengyao[u"破军"]) \
            and (huayao[u"化忌"][0] in sfsz(zhengyao[u"破军"]) or (shayao[u"火星"] in sfsz(zhengyao[u"破军"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"破军"]) \
                or shayao[u"擎羊"]  in sfsz(zhengyao[u"破军"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"破军"]))):
        result.append (u"破军财帛位，如汤浇雪。（注）无禄见煞忌者始是。")
    if  zhengyao[u"破军"] in sfsz(gwzhi[7]) and fuyao[u"天马"] in sfsz(zhengyao[u"破军"]) and (shayao[u"火星"] in sfsz(zhengyao[u"破军"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"破军"])):
        result.append (u"破军居奴仆，谤怨私逃。（注）见天马火铃方是。")
    if  zhengyao[u"破军"] == gwzhi[9] and (huayao[u"化忌"][0] in sfsz(zhengyao[u"破军"]) or (shayao[u"火星"] in sfsz(zhengyao[u"破军"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"破军"]) \
         or shayao[u"擎羊"]  in sfsz(zhengyao[u"破军"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"破军"]))):
        result.append (u"破军居田宅，祖基破荡。（注）见煞始是。")
    if  zhengyao[u"破军"] in (gwzhi[10],gwzhi[11]) and (huayao[u"化忌"][0] in sfsz(zhengyao[u"破军"]) or (shayao[u"火星"] in sfsz(zhengyao[u"破军"]) or shayao[u"铃星"]  in sfsz(zhengyao[u"破军"]) \
         or shayao[u"擎羊"]  in sfsz(zhengyao[u"破军"]) or shayao[u"陀罗"]  in sfsz(zhengyao[u"破军"]))):
        result.append (u"破军居福德父母，刑克破相。（注）见煞者是，尤忌火铃。父母宫又名相貌宫。故有破相之应。")
    return result

def zuoyou_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '辅弼'
    if xiangjia(mgindex,fuyao[u"左辅"],fuyao[u"右弼"]):
        result.append (u"左右文昌，位至合辅。（注）须原命宫吉始是。")
    if xiangjia(mgindex,fuyao[u"左辅"],fuyao[u"右弼"]) and mgindex == zhengyao[u"天相"] or (mgindex == zhengyao[u"紫薇"] and zhengyao[u"紫薇"] == zhengyao[u"破军"]):
        result.append (u"左右夹命为贵格。（注）命宫为「紫破」始是。天相亦可。（见卷二图8）")
    #左辅右弼，终身福厚。（注）北仅为助禄。
    if mgindex == zhengyao[u"紫薇"] and zhengyao[u"紫薇"] == zhengyao[u"破军"] and mgindex == fuyao[u"左辅"] and mgindex == fuyao[u"右弼"]:
        result.append (u"左右同宫，披罗衣紫。（注）命宫为「紫破」始是。（见卷一第75页）")
    #左右单守照命宫，离宗庶出。（注）以右弼为的，然尚须见火铃。（见图30）
    if mgindex == zhengyao[u"天相"] and fuyao[u"右弼"] == zhengyao[u"天相"] and (huayao[u"化禄"][0] == zhengyao[u"巨门"] or (zhengyao[u"巨门"] in (3,9) and huayao[u"化权"][0] == zhengyao[u"天梁"])\
        or (zhengyao[u"巨门"] in (2,8) and huayao[u"化禄"][0] == zhengyao[u"太阳"])  or (zhengyao[u"天同"] in (1,7) and huayao[u"化禄"][0] == zhengyao[u"太阳"])):
        #最正宗“财荫夹印”格是巨门化禄，与天梁一起夹天相。因为按照安星诀的说法，天梁必在天相的前一宫，而巨门必在天相的后一宫。另外，天机化禄和天梁化权夹天相，亦为大吉，不单是财荫夹，而且是禄权夹。
        # 太阳化禄和天梁夹宫亦佳，更次之的，是天同化禄天梁夹，财气较弱，助力也较逊色。禄存和天梁夹宫，虽然也有财荫夹的性质，但由于必有擎羊同度，擎羊化气为刑，不利天相，故为破格
        result.append (u"财荫夹印")
        if fuyao[u"右弼"] == zhengyao[u"天相"]:
            result.append (u"右弼天相福来临。（见卷二第194页）（注）须兼得「财荫夹印」者尔是。")
    if fuyao[u"左辅"] == fuyao[u"右弼"] and fuyao[u"左辅"] in (gwzhi[4],gwzhi[10]):
        result.append (u"左右财官兼夹棋，衣禄丰盈。（注）此言财帛宫或福德宫，与左右同，或左右火者，主如此克应。然此亦仅为助缘。")
    #左右魁钺为福寿。（注）此亦仅为助缘。
    if (mgindex == fuyao[u"左辅"] and fuyao[u"左辅"] == fuyao[u"文昌"] and shayao[u"擎羊"]  in sfsz(mgindex)) \
        or (mgindex == fuyao[u"右弼"] and fuyao[u"右弼"] == fuyao[u"文曲"] and shayao[u"陀罗"]  in sfsz(mgindex)):
        result.append (u"左右昌曲逢羊陀，当生异痣。（注）昌左羊为一组，曲右陀为一组。若溷杂即不是。")
    #左右魁皱，禄扶为奇。（注）四辅曜以得禄为贵。
    #左右贞羊遭刑盗。（注）廉贞化忌为的。
    if fuyao[u"左辅"] == fuyao[u"右弼"] and mgindex == fuyao[u"左辅"] and fuyao[u"左辅"]  in (4,10,1,7):
        result.append (u"墓逢左右，八座之尊。（注）左辅右弼入庙于辰戌丑未四墓宫。（见图31）")
    if fuyao[u"左辅"] in sfsz(mgindex) and zhengyao[u"紫薇"] in sfsz(mgindex) and zhengyao[u"天相"] in sfsz(mgindex) and  fuyao[u"右弼"] in sfsz(mgindex) \
        and not(shayao[u"火星"] in sfsz(mgindex) and shayao[u"火星"] == huayao[u"化禄"][0]):
        result.append (u"左辅紫府相，右弼来会。一生富贵双全。（注）见火星化忌冲破，结局不佳。")
    if mgindex == fuyao[u"右弼"] and mgindex == zhengyao[u"紫薇"]  and mgindex == zhengyao[u"天府"]  and shayao[u"铃星"] not in sfsz(mgindex):
        result.append (u"右弼紫府同宫，财官双美。（注）见铃星冲破，结局不佳。")
    if mgindex == fuyao[u"左辅"] and zhengyao[u"紫薇"]  in sfsz(mgindex) and zhengyao[u"天府"]  in sfsz(mgindex) and fuyao[u"禄存"]  in sfsz(mgindex):
        result.append (u"左辅守命，紫府禄存三合拱照，文武大贵。（注）煞忌减贵。")
    if mgindex == fuyao[u"右弼"] and zhengyao[u"天府"]  in sfsz(mgindex) and zhengyao[u"天相"]  in sfsz(mgindex)  and fuyao[u"文昌"]  in sfsz(mgindex) \
         and fuyao[u"文曲"]  in sfsz(mgindex):
        result.append (u"右弼守命，会府相昌曲，终身福厚。（注）同前。")
    #左辅机昌亦主贵。（注）同前「左辅紫府相」注。
    #左辅日月、贪武合，终身利禄有声名。（注）化忌则不入格。
    if fuyao[u"左辅"] == gwzhi[2]:
        result.append (u"左辅守夫妻，人定二婚。（见图32）（注）见煞忌主死别。见火铃则生离。")
    if fuyao[u"右弼"] == gwzhi[2]:
        result.append (u"右弼守夫妻，人定二婚。（见图33）（注）同前。")
    if mgindex == fuyao[u"左辅"] and shayao[u"擎羊"]  in sfsz(mgindex) and shayao[u"铃星"]  in sfsz(mgindex) and ((mgindex == zhengyao[u"巨门"] and mgindex == zhengyao[u"巨门"]) or mgindex == zhengyao[u"七杀"]):
        result.append (u"左辅守命羊铃凑，巨机七杀为下局。（注）正曜为七杀或「巨门天机」者是。")
    if mgindex == fuyao[u"左辅"] and shayao[u"擎羊"]  in sfsz(mgindex) and shayao[u"铃星"]  in sfsz(mgindex) and (kongyao[u"地劫"] in sfsz(mgindex) or kongyao[u"地空"] in sfsz(mgindex)):
        result.append (u"左辅同会煞重重，有始无终。（注）尤忌羊铃空劫。")
    if mgindex == fuyao[u"右弼"] and shayao[u"火星"]  in sfsz(mgindex) and shayao[u"陀罗"]  in sfsz(mgindex) and (kongyao[u"地劫"] in sfsz(mgindex) or kongyao[u"地空"] in sfsz(mgindex)):
        result.append (u"右弼同会煞重重，有福难享。（注）尤忌火陀空劫。")
    return result

def kuiyue_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '魁钺'
    if (fuyao[u"天魁"] == mgindex and fuyao[u"天钺"] == gwzhi[6]) or (fuyao[u"天魁"] == gwzhi[6] and fuyao[u"天钺"] == mgindex):
        result.append (u"魁钺坐贵向贵，左右吉聚富而贵。（注）命宫与对宫有魁钺，更得吉拱。（见卷二图26）")
    if fuyao[u"天魁"] == mgindex and fuyao[u"天钺"] == sgindex and shayao[u"火星"] not in sfsz(mgindex) \
        and shayao[u"铃星"] not in sfsz(mgindex) and shayao[u"擎羊"] not in sfsz(mgindex) and shayao[u"陀罗"] not in sfsz(mgindex):
        result.append (u"魁临命，钺临身，少年必娶美妻。（注）无煞始是。（见图34）")
    if fuyao[u"天魁"] == sgindex and fuyao[u"天钺"] == mgindex and huayao[u"化忌"][0] not in sfsz(mgindex) and huayao[u"化科"][0] not in sfsz(mgindex):
        result.append (u"魁铍身命，盖世文章。（见卷二第62页）（注）须不见化忌，且见科星。")
    if fuyao[u"天魁"] == fuyao[u"天钺"] and fuyao[u"天魁"] == mgindex:
        result.append (u"魁钺同行，位至台辅。（见卷一第48页）。（注）若仅三方会合则不是。")
    #魁钺命身多折桂。（注）分躔命身宫始是。参前注。
    if xiangjia(mgindex,fuyao[u"天魁"],fuyao[u"天钺"]):
        result.append (u"魁钺夹命为奇格。（注）见《骨髓赋》注（即卷二第16页）。")
    #贵入贵乡，逢之富贵。（注）原局魁钺，运限又迭并魁钺。
    if fuyao[u"天魁"] in sfsz(mgindex) and fuyao[u"天钺"] in sfsz(mgindex) and fuyao[u"文昌"] in sfsz(mgindex) and fuyao[u"文曲"] in sfsz(mgindex) \
            and fuyao[u"禄存"] in sfsz(mgindex) and huayao[u"化忌"][1] not in(u"文昌",u"文曲"):
        result.append (u"魁钺昌曲禄存扶，刑煞无冲台辅贵。（注）昌曲须不化忌。")
    if mgindex in (fuyao[u"天魁"],fuyao[u"天钺"]):
        result.append (u"魁钺辅星为福寿。（注）魁钺为辅星，入命宫，主增福寿。")
    if fuyao[u"天魁"] in sfsz(mgindex) and fuyao[u"天钺"] in sfsz(mgindex) and (shayao[u"擎羊"]  in sfsz(mgindex)  or shayao[u"陀罗"]  in sfsz(mgindex)):
        result.append (u"魁钺重逢羊陀，痼疾尤多。（注）原局魁钺有羊陀，行至羊陀迭并之运限。主沉疴痼疾。")
    if fuyao[u"天魁"] in sfsz(mgindex) and fuyao[u"天钺"] in sfsz(mgindex) and fuyao[u"左辅"] in sfsz(mgindex) and fuyao[u"右弼"] in sfsz(mgindex):
        result.append (u"魁钺辅弼三方，一生遇贵提携。（注）四曜在三方四正相会，无煞忌，谋为毫不费力。")
    return result

def changqu_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '昌曲'
    if fuyao[u"文曲"] in sfsz(mgindex) and fuyao[u"文昌"] in sfsz(mgindex) and zhengyao[u"武曲"] in sfsz(mgindex):
        result.append (u"昌曲文昌武曲。为人多学多能。（注）参见武曲「武曲相遇昌曲逢」条。（见第20页）")
    if fuyao[u"文曲"] in sfsz(mgindex) and fuyao[u"文昌"] in sfsz(mgindex) and zayao[u"龙池"] in sfsz(mgindex) \
        and zayao[u"凤阁"] in sfsz(mgindex) and zayao[u"天才"]  in sfsz(mgindex) and huayao[u"化科"][0]  in sfsz(mgindex):
        result.append (u"文科拱照，贾谊年少登科。（卷二图41）（注）指昌曲、龙池凤阁、天才、化科。")
    if fuyao[u"文昌"] == mgindex and fuyao[u"左辅"] == mgindex:
        result.append (u"文昌左辅，位至三合。（见卷二第67页）（注）此言昌优于曲，辅胜于弼。")
    if fuyao[u"文昌"] in (mgindex,sgindex) and zhengyao[u"武曲"] in (mgindex,sgindex) and fuyao[u"文昌"] in (2,8) and fuyao[u"武曲"] in (2,8):
        result.append (u"文昌武曲于身命，文武兼贫。（注）亦必寅申宫方是。（见图35）")
    if zhengyao[u"武曲"] in (1,4) and fuyao[u"文曲"] in (1,4) and mgindex in (1,4):
        result.append (u"二曲庙旺逢左右，将相之材。（见图36）（注）二曲指武曲文曲。然中洲派所传，则仅指丑、辰二宫。丑宫较优。")
        #二曲旺宫，威名显赫。（注）同前。
    if mgindex in (1,6) and fuyao[u"文曲"] in sfsz(mgindex) and zhengyao[u"武曲"] in sfsz(mgindex) and zhengyao[u"贪狼"] in sfsz(mgindex) \
            and (shayao[u"火星"] in sfsz(mgindex) or shayao[u"铃星"]  in sfsz(mgindex) \
            or shayao[u"擎羊"]   in sfsz(mgindex) or shayao[u"陀罗"]  in sfsz(mgindex) or huayao[u"化忌"][0]  in sfsz(mgindex)):
        result.append (u"二曲贪狼午丑限，防溺水之忧。（注）见煞忌方是。命在丑者防丑限，命在未者防午限。")
    if xiangjia(mgindex,fuyao[u"文曲"],fuyao[u"文昌"]):
        result.append (u"昌曲夹命最为奇。（见图37）（注）命宫须见吉化。")
    if (fuyao[u"文昌"] in sfsz(mgindex) and fuyao[u"左辅"] in sfsz(mgindex) and shayao[u"擎羊"]  in sfsz(mgindex)) \
        or (fuyao[u"文曲"] in sfsz(mgindex) and fuyao[u"右弼"] in sfsz(mgindex) and shayao[u"陀罗"]  in sfsz(mgindex)):
        result.append (u"昌曲左右会羊陀，当生异痣。（注）昌左羊为一组，曲右陀为一组。若溷杂即不是。")
    #女人昌曲，聪明富贵且多淫。（注）昌曲仅为助缘，非主因。
    if fuyao[u"文昌"] == mgindex and fuyao[u"文曲"] == mgindex and fuyao[u"破军"] == mgindex \
        and (shayao[u"火星"] in sfsz(mgindex) or shayao[u"铃星"]  in sfsz(mgindex) \
        or shayao[u"擎羊"]   in sfsz(mgindex) or shayao[u"陀罗"]  in sfsz(mgindex) or huayao[u"化忌"][0]  in sfsz(mgindex)):
        result.append (u"昌曲破军同宫，主水厄。（注）见煞始是。（见卷一第91页）")
    if fuyao[u"文昌"] == mgindex and zhengyao[u"贪狼"] == mgindex and ygindex == 7:
        result.append (u"文昌贪狼，政事颠倒。（注）文曲化科、文昌化忌始是。")
    if fuyao[u"文昌"] == mgindex and zhengyao[u"巨门"] == mgindex and ygindex == 7:
        result.append (u"文昌巨门多丧志。（注）同前。")
    if fuyao[u"文昌"] in (1,7) and fuyao[u"文曲"] in (1,7):
        result.append (u"昌曲临于丑未。时逢卯酉近天颜。（注）命在丑，限逢酉；命在未，限逢卯。又须原局运限皆见吉化。主能近贵人。")
    if (fuyao[u"文昌"] in (5,11) and fuyao[u"文昌"] in (zhengyao[u"紫薇"],zhengyao[u"天府"])) \
            or  ( fuyao[u"文曲"] in (5,11) and fuyao[u"文曲"] in (zhengyao[u"紫薇"],zhengyao[u"天府"])):
        result.append (u"昌曲巳亥临，不贵即大富。（注）此言与「紫微七杀」或天府同躔。（见图38）")
    if mgindex == zhengyao[u"紫薇"] and mgindex == 6 and gwzhi[10] in (fuyao[u"文昌"],fuyao[u"文曲"]):
        result.append (u"昌曲吉星居福德，称为玉袖天香。（注）必须紫微为命宫始是。以午为佳。（见图39）")
    #昌曲陷宫凶煞破，虚誉之隆。（注）凶煞指四煞空劫。
    #昌曲陷于天殇，颜回夭折。（注）此条不确。（见卷二第104页）
    if fuyao[u"文昌"] in sfsz(mgindex) and fuyao[u"文曲"] in sfsz(mgindex) and ygindex in (5,7,8):
        result.append (u"昌曲己辛壬生人，限逢辰戌虑投河。（注）此实言武曲文曲双化忌主有意外。")
    if mgindex == zhengyao[u"廉贞"] and fuyao[u"文昌"] in (5,11) and fuyao[u"文昌"] == fuyao[u"文曲"] and fuyao[u"文昌"] == zhengyao[u"廉贞"] and huayao[u"化忌"][1]  in (u"文昌",u"文曲"):
        result.append (u"昌曲廉贞于巳亥，遭刑不善且虚夸。（见卷二图59）（注）巳亥「廉贪」见文昌或文曲化忌。")
    if mgindex == fuyao[u"文昌"] and fuyao[u"文昌"] == fuyao[u"文曲"] and mgindex == fuyao[u"禄存"]:
        result.append (u"昌曲禄存，尤为奇特。（注）昌曲宜见禄，否则虚名。")
    if zhengyao[u"破军"] in (2,3) and zhengyao[u"破军"] == fuyao[u"文昌"] and zhengyao[u"破军"] == fuyao[u"文曲"] \
            and (shayao[u"火星"] in sfsz(mgindex) or shayao[u"铃星"]  in sfsz(mgindex) \
            or shayao[u"擎羊"]   in sfsz(mgindex) or shayao[u"陀罗"]  in sfsz(mgindex)):
        result.append (u"昌曲破军临虎兔，煞羊冲破奔波。（见卷一第78页）（注）寅卯二宫破军昌曲，忌四煞冲破。")
    if zhengyao[u"廉贞"] in (1,7) and zhengyao[u"廉贞"] in (shayao[u"擎羊"],shayao[u"陀罗"]) and fuyao[u"文昌"] == zhengyao[u"廉贞"]:
        result.append (u"文昌廉杀羊陀，为人诈伪。（见图40）（注）此指丑未宫「廉杀」有羊陀同，更见文昌。")
    if fuyao[u"文曲"]  in (mgindex,sgindex) or fuyao[u"文昌"]  in (mgindex,sgindex):
        result.append (u"文曲单居身命，逢凶曜舌辩之徒。（注）若文昌如此，则虽舌辩而有高艺。")
    return result

def huayao_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    '禄马'
    if fuyao[u"禄存"] in (gwzhi[4],gwzhi[9]) and huayao[u"化禄"][0] in sfsz(fuyao[u"禄存"]):
        result.append (u"禄马禄存守于财宅，积玉堆金。（注）必同会化禄始是。")
    if fuyao[u"禄存"] in (0,6) and fuyao[u"禄存"] in (mgindex,sgindex):
        result.append (u"禄存子午位迁移，身命逢之利禄宜。（注）禄存在子，马在申；禄存在午，马在寅。为迁移宫。")
#明禄暗禄，位至公卿。（注）此言二禄同宫。或在六合位。（见卷二第158页）
    if mgindex == fuyao[u"禄存"] and fuyao[u"禄存"] == huayao[u"化禄"][0]:
        result.append (u"双禄重逢，终身富贵。（注）同上。双禄守命，吕后专权。（见卷二图50）（注）同上。")
    if mgindex in (fuyao[u"禄存"],(fuyao[u"禄存"]+6)%12)  and fuyao[u"禄存"] in (fuyao[u"天马"],(fuyao[u"天马"]+6)%12) and shayao[u"火星"] not in sfsz(mgindex) \
            and shayao[u"铃星"]  not in sfsz(mgindex) and kongyao[u"地劫"]  not in sfsz(mgindex) and kongyao[u"地空"]  not in sfsz(mgindex) and zayao[u"正空"]  not in sfsz(mgindex):
        result.append (u"禄存厚重多衣禄。（注）此言女命。（见卷二第195页）禄马最喜交驰。（见卷一第20页及卷二第64页）（注）禄马同宫，或禄马对冲皆是。唯不宜见火铃空劫，亦不宜见正截空，否则仅主奔波。")
    if mgindex == fuyao[u"禄存"] and fuyao[u"禄存"] in sfsz(mgindex) and huayao[u"化忌"][0] in sfsz(mgindex)  and huayao[u"化忌"][1] in (u"文昌",u"文曲"):
        result.append (u"禄逢冲破，吉也成凶。（见卷一第22页）（注）最忌昌曲化忌冲禄，因财招祸。")
    #天马四生妻宫，富贵还当封赠。（注）天马必居四长生位，故此句无理。
    if fuyao[u"天马"] in sfsz(mgindex) and (kongyao[u"地劫"] in sfsz(mgindex) or kongyao[u"地空"] in sfsz(mgindex) or zayao[u"正空"] in sfsz(mgindex)):
        result.append (u"马遇空亡，终身奔走。（见卷一第26页）（注）此指地空、地劫，亦指正截空而言，天空旬空不论。")
    if mgindex == fuyao[u"禄存"]:
        result.append (u"禄存独守命，无言化作守财奴。（见图41）（注）见煞则财难守，仅主吝啬。")
    if fuyao[u"禄存"] in sfsz(mgindex) and fuyao[u"禄存"] in (kongyao[u"地劫"],kongyao[u"地空"]) and shayao[u"火星"]  in sfsz(mgindex) and shayao[u"铃星"]  in sfsz(mgindex):
        result.append (u"禄存落空亡之地，凑火铃巧艺安身。（见图42）（注）空亡指地劫地空。")
    if gwzhi[2] in (fuyao[u"禄存"],huayao[u"化禄"][0]) and fuyao[u"禄存"] in sfsz(gwzhi[2]) and huayao[u"化禄"][0] in sfsz(gwzhi[2]):
        result.append (u"合禄鸳鸯一世荣。（注）禄存或化禄，一守夫妻宫，另一在三方来合。（另文详见卷二第149页）禄居奴仆，纵有官也奔驰。（注）见《太微赋》注。（即卷一第93页）")
    '科禄权'
    if (huayao[u"化禄"][0] in sfsz(mgindex) and huayao[u"化权"][0] in sfsz(mgindex) and huayao[u"化科"][0] in sfsz(mgindex)) \
        or (huayao[u"化禄"][0] in sfsz(sgindex) and huayao[u"化权"][0] in sfsz(sgindex) and huayao[u"化科"][0] in sfsz(sgindex)):
        result.append (u"科禄权会守身命，出将入相。（注）是谓「禄权科会」。（见卷二第45页）")
    if (xiangjia(mgindex,huayao[u"化禄"][0],fuyao[u"禄存"]) and huayao[u"化忌"][0] not in sfsz(mgindex)) \
            or (xiangjia(sgindex,huayao[u"化禄"][0],fuyao[u"禄存"]) and huayao[u"化忌"][0] not in sfsz(sgindex)):
        result.append (u"化禄禄存夹身命，不贵则富。（见图43）（注）无化忌始是，见煞减等")
    if (xiangjia(mgindex,huayao[u"化权"][0],huayao[u"化科"][0]) and huayao[u"化忌"][0] not in sfsz(mgindex)) \
            or (xiangjia(sgindex,huayao[u"化权"][0],huayao[u"化科"][0]) and huayao[u"化忌"][0] not in sfsz(sgindex)):
        result.append (u"化权化科夹身命，富贵声扬。（见图44）（注）同上。")
    if huayao[u"化禄"][0] in sfsz(mgindex) and huayao[u"化权"][0] in sfsz(mgindex) \
            and  (shayao[u"火星"] in sfsz(mgindex) or shayao[u"铃星"]  in sfsz(mgindex) \
            or shayao[u"擎羊"]   in sfsz(mgindex) or shayao[u"陀罗"]  in sfsz(mgindex)):
        result.append (u"权禄重逢逢煞凑，虚誉之隆。（注）化禄化权同会，见四煞。")
    if gwzhi[7] in (huayao[u"化禄"][0],huayao[u"化权"][0]):
        result.append (u"权禄吉星奴仆位，纵然富贵也奔驰。（注）同《太微赋》「禄居奴仆」注(即卷一第93页)。")
    if huayao[u"化权"][0] in sfsz(mgindex) and (shayao[u"擎羊"]   in sfsz(mgindex) or shayao[u"陀罗"]  in sfsz(mgindex) \
       or kongyao[u"地劫"]  in sfsz(mgindex) or kongyao[u"地空"]  not in sfsz(mgindex)):
        result.append (u"化权遇羊陀空劫,见天使主因谗受谪。（注）天使为奴仆谗言之应。")
    if huayao[u"化科"][0] in (mgindex,sgindex):
        result.append (u"化科守身命，逢恶曜亦为文士。（注）但贫寒。化科独嫌天空旬空，遇则虚名。（注）主有名无利。")
    #科权对拱，跃三汲于禹门。（见卷二第72页）（注）二曜相对，科第易得。（见图45）
    #科明禄暗，位列三台。（注）化科守命，禄在六合位来合。如子丑合、寅亥合之类。（见卷二第49页）
    if huayao[u"化科"][0] in sfsz(mgindex) and huayao[u"化科"][0] in (5,9):
        result.append (u"科文陷于凶乡，苗而不秀。（见卷二第36页）（注）主有虚名而无实学。")
    '化忌'
    if huayao[u"化忌"][0] in (mgindex,sgindex) and (shayao[u"火星"] in sfsz(mgindex) or shayao[u"铃星"]  in sfsz(mgindex) \
            or shayao[u"擎羊"]   in sfsz(mgindex) or shayao[u"陀罗"]  in sfsz(mgindex)):
        result.append (u"化忌命身宫，作事不亨通。（注）见煞始是。")
    #日月庙旺，化忌为福。（注）化忌反可潜藏，否则锋芒太露。
    #日月陷地，化忌刑伤。（注）主刑六亲，伤眼目等。
    if huayao[u"化忌"][1] == u"廉贞" and zhengyao[u"廉贞"] in sfsz(mgindex) and zhengyao[u"廉贞"] == 5:
        result.append (u"廉贞化忌于陷地，无成且主遭刑。（注）廉贞陷于巳，唯子午卯酉平闲亦不利。")
    return result

def shayao_rule(sex,ygindex,yzindex,hzindex
    ,mgindex,sgindex,whindex,whju,sgganindex,gwgan,gwzhi,zhengyao,fuyao,shayao,huayao,kongyao,zayao,changsheng12,taisui12,jiangqian12,boshi12):
    result =[]
    if (shayao[u"擎羊"] in sfsz(mgindex) and shayao[u"擎羊"] in (1,4,7,10)) \
        or (shayao[u"陀罗"] in sfsz(mgindex) and shayao[u"陀罗"] in (1,4,7,10)):
        result.append (u"羊陀擎羊入庙，富贵声扬。（注）见吉化始的。")
    if shayao[u"擎羊"] == shayao[u"火星"] and shayao[u"擎羊"] in sfsz(mgindex) and shayao[u"擎羊"] in (4,10):
        result.append (u"羊火同宫，威权压众。（见卷二第101页）（注）辰戌二宫始是。此为火炼真金。")
    if (shayao[u"擎羊"]  in sfsz(mgindex) and shayao[u"陀罗"]  in sfsz(mgindex) and shayao[u"火星"] in sfsz(mgindex) and shayao[u"铃星"]  in sfsz(mgindex))\
       or (shayao[u"擎羊"]  in sfsz(sgindex) and shayao[u"陀罗"]  in sfsz(sgindex) and shayao[u"火星"] in sfsz(sgindex) and shayao[u"铃星"]  in sfsz(sgindex)) :
        result.append (u"羊陀铃火守身命，腰驼曲背之人。（注）此言四煞同会命宫。（见图46）")
    if shayao[u"擎羊"]  in sfsz(mgindex) and shayao[u"擎羊"] in (0,6,4,9):
        result.append (u"擎羊子午卯酉，非夭折即刑伤。（注）子午卯酉四仲位，为擎羊陷宫 然此条言过其实")
    #擎羊逢力士，李广难封。（注）此条无理。盖凡阳男阴女守命四旺宫必见此格。（见卷二图44）
    if xiangjia(mgindex,shayao[u"擎羊"],shayao[u"陀罗"]):
        result.append (u"羊陀夹忌为败局。（注）不只命宫，行至运限亦然。")
    if mgindex == shayao[u"擎羊"] and shayao[u"擎羊"] == shayao[u"铃星"]:
        result.append (u"羊铃坐命，流年白虎灾伤。（注）流年到原局命宫，白虎又到。（见卷一第141页）")
    #擎羊对守在酉宫，岁迭羊陀庚命凶。（注）此不过举「羊陀迭并」之例。
    #羊陀流年铃，破面字斑痕。（注）原局铃星，流年羊陀来夹，主受刑。
    #擎羊重逢流羊，西施倾命陨身。（注）此亦「举陀迭并」。
    if zhengyao[u"太阳"] in (1,7) and shayao[u"擎羊"] == zhengyao[u"太阳"] and huayao[u"化忌"][0] == zhengyao[u"太阳"]:
        result.append (u"擎羊日月同宫，男克妻而女刑夫。（注）男太阴化忌（见图47），女太阳化忌。")
    #擎羊昌曲左右同，斑痕暗痣。（注）参见昌曲左右会羊陀注。（见本卷第68页）
    return result
    '''
擎火廉贞巨门同。伤残暗疾且招刑。（注）廉贞见羊火且化忌，或巨门见羊火且化忌，主有此应。（见卷二第137页
擎羊独守，火忌劫空冲破，残疾离祖刑伤。（注）坏在天同化忌。
陀罗独守，二姓延生。（注）火星同躔尤甚。
陀罗守命，巧艺安身。（注）须不见煞忌。见昌曲尤佳。
陀罗守命同日月，男克妻而女刑夫。（见图48）（注）参见擎羊条。
陀罗陷宫逢杀巨，伤残带疾且刑伤。（注）指寅申巳亥四宫。
陀罗贪狼坐命寅，伶俐风流。（注）参见「风流彩杖」条。（见卷一第87页）
陀罗贪狼同身命，酒色成痨。（注）见桃花诸曜始是。
陀罗火铃同宫，疫瘟而死。（注）指传染病。
陀罗守命，齿舌遭伤。（注）或牙齿畸型。
陀罗巳亥寅申，非夭折即刑伤。（注）巳亥寅申四孟宫，为陀罗陷宫，亦言过其实。
火铃
火铃相遇，名振诸邦。
（注）不确，凡申子辰年生人必火铃相会。（见图49）
火铃夹命为败局。
（注）仅不宜夹忌。（见图50）
火铃旺富亦为福。
（注）旺富指寅午戌。
火陀铃羊为下格，孤单弃祖或伤残。
（注）陀罗不宜火星，擎羊则忌铃星。
火铃陷地羊陀同，过房二姓延生。
（注）参见前条。
女命火星独守，凌夫克子是非多。
（注）福德宫亦凶始是。
女命铃星独守，外贤淑而内心狠毒。
（注）同前注。
火铃贪狼四墓宫，三方吉拱立边功。
（注）辰戌丑未宫之火贪、铃贪格。（见卷二第61页）
火星守命朝紫府，不贵亦富。
（注）须紫府有百官朝拱。
铃星守命朝紫府，阵上亡身。（注）火星可制七杀，铃星不能制。
火铃同宫共擎羊，廉贞七杀阵中亡。
（注）此指铃羊或火羊而言。
铃昌陀武，限至投河。
（注）四星交会辰戌，若化忌者是。（见卷二第135页）
'''

def save_zwrule(selsql='select id,sex,lyear,lmonth,lday,leap,ygindex,yzindex,hzindex from mingzhu '
                ,delsql="delete from zwrule where pid=%d;"
                ,updsql = "insert into zwrule(pid,ruletype,rule) \
                values(%d,'%s','%s')"):
    results=sh.ExecQuery(selsql)
    for result in results:
        try:
            id,sex,lyear,lmonth,lday,leap,ygindex,yzindex,hzindex=result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8]
            sql = delsql % (id);
            sh.ExecNonQuery(sql)
            bx_result,tw_result,xt_result = baxl_rule(lyear,lmonth,lday,leap,ygindex,yzindex,hzindex,sex)
            sqls = []
            if bx_result <> None:
                for r in bx_result:
                    sqls.append(updsql % (id,u"八喜楼",r))
                sh.ExecNonQuery(';'.join(sqls))
            if tw_result <> None:
                for r in tw_result:
                    sqls.append(updsql % (id,u"太微赋",r))
                sh.ExecNonQuery(';'.join(sqls))
            if xt_result <> None:
                for r in xt_result:
                    sqls.append(updsql % (id,u"形体赋",r))
                sh.ExecNonQuery(';'.join(sqls))

        except Exception,e:
            print 'error:',e.message,traceback.format_exc()

if __name__ == '__main__':
    #baxl_rule()
    save_zwrule()
