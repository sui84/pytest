#coding=utf-8
import time

from werobot import WeRoBot

import confhelper
import fhelper
from pytest.pytest.utils.DB import sqlhelper

if __name__ == '__main__':
    print time.ctime(), 'Start...'
    # region Data
    ipTable = ['158.59.194.213', '18.9.14.13', '58.59.14.21']
    headers = ('area', 'user', 'recharge')
    data = [
        ('1', 'Rooney', 20),
        ('2', 'John', 30),
    ]
    dictObj = {
	'andy':{
		'age': 23,
		'city': 'shanghai',
		'skill': 'python'
	},
	'william': {
		'age': 33,
		'city': 'hangzhou',
		'skill': 'js'
	}
    }
    dictObj2 = {
	'andy2':{
		'age': 23,
		'city': 'shanghai',
		'skill': 'python'
	},
	'william2': {
		'age': 33,
		'city': 'hangzhou',
		'skill': 'js'
	}
    }
    dictListObj = [dictObj,dictObj2]
    # endregion
    try:
        f = fhelper.FHelper(filename=r'd:\temp\test.csv')
        f.GetAllLines()

        conf = confhelper.ConfHelper(u'd:/TEMP/test.conf')
        conf.GetAllConfig()
        conf.GetSectionConfig('db')
        print conf.GetConfig('db','host')
        # mg = mghelper.MgHelper()

        #region tablib 应用
        #data = tablib.Dataset(*data, headers=headers)
        #然后就可以通过下面这种方式得到各种格式的数据了。
        # data.xlsx
        # data.xls
        # data.ods
        # data.json
        # data.yaml
        # data.csv
        # data.tsv
        # data.html
        #endregion

        #region fhelper应用
        # f = fhelper.FHelper(filename=r'd:\temp\test.csv')
        #  f.SaveDict(dictObj)
        # f2 = fhelper.FHelper()
        #f2.SaveDictList(dictListObj)
        #endregion

        #region mghelper应用
        #mg.SaveFile( r'd:\temp\test.csv')  # 保存json文件到mongodb
        # mg.SaveRow(dictListObj)
        # itchat.auto_login(enableCmdQR=2)
        #endregion

        #region mssql应用
        ## ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
        ## #返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
        ## ms.ExecNonQuery("insert into WeiBoUser values('2','3')")

        ms = sqlhelper.SqlHelper(host=r"localhost\SQLEXPRESS", user="sa", pwd="pwd", db="dbname")
        resList = ms.ExecQuery("SELECT * FROM test")

        #endregion

        # region itchat应用
        # itchat.auto_login(enableCmdQR=True)
        # 获取朋友到DB
        # mfs = itchat.get_friends()
        # mg.SaveDictObjs(mfs)
        # 获取朋友到CSV , 因为自己比其它多了个Uin，所以必须去掉
        # mfs[0].pop('Uin')
        # f = fhelper.FHelper(filename=r'd:\temp\test.csv')
        # f.SaveDictListToCSV(mfs)
        # # 获取公众号
        # mps = itchat.get_mps()
        # mg.SaveDictObjs(mps)
        # #  获取群聊--不完整！
        # crs=itchat.get_chatrooms()
        # mg.SaveDictObjs(crs)
        # #
        # cs=itchat.get_contact()
        # mg.SaveDictObjs(cs)
        #
        # # 发送信息
        # users=itchat.search_friends(name=u'猪猪良')
        # username=users[0]['UserName']
        # itchat.send(u'小喳喳',toUserName=username)

        # endregion

        # region itchatmp
        # itchatmp.update_config(itchatmp.WechatConfig(
        #     token='bUiy1ZwNDNBSIRIxOGPqpojOc9JIcfGRMAs8J1Ww9xyL6Z8nyz9cLdNDnSfuW-3x_Oy2E3ZGYARjo8QqHl-d29LFWFMyINWKX97-Rahc-Yny3g6CMBf3OQOC40lAJXUHVHCcABAGSN',
        #     appId = 'wx675d68299018008f',
        #     appSecret = '5436fb3ceb9fa60cd9685fe70066305b'))
        #
        # @itchatmp.msg_register(itchatmp.content.TEXT)
        # def text_reply(msg):
        #     print msg
        #     return msg['content']
        # itchatmp.run()
         # endregion应用



        #region werobot
        robot = WeRoBot(enable_session=False,
                        token='bUiy1ZwNDNBSIRIxOGPqpojOc9JIcfGRMAs8J1Ww9xyL6Z8nyz9cLdNDnSfuW-3x_Oy2E3ZGYARjo8QqHl-d29LFWFMyINWKX97-Rahc-Yny3g6CMBf3OQOC40lAJXUHVHCcABAGSN',
                        APP_ID='wx675d68299018008f',
                        APP_SECRET='5436fb3ceb9fa60cd9685fe70066305b')

        @robot.handler
        def hello(message):
            return 'Hello world'
        robot.run()
        #endregion



    except Exception,e:
        print time.ctime(), 'Error!'
        print e.message
    finally:
        print time.ctime(), 'Done!'
