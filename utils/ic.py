#coding=utf-8
import itchat
#from itchat.content import *

# @itchat.msg_register([PICTURE,TEXT])
# def simple_reply(msg):
    # if msg['Type'] == TEXT:
        # ReplyContent = 'I received message: '+msg['Content']
    # if msg['Type'] == PICTURE:
        # ReplyContent = 'I received picture: '+msg['FileName']
    # itchat.send_msg('nice to meet you',msg['FromUserName'])
itchat.auto_login(enableCmdQR=2)
itchat.run()

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

 # itchat.auto_login(enableCmdQR=2)


        #region werobot
        # robot = WeRoBot(enable_session=False,
                        # token='bUiy1ZwNDNBSIRIxOGPqpojOc9JIcfGRMAs8J1Ww9xyL6Z8nyz9cLdNDnSfuW-3x_Oy2E3ZGYARjo8QqHl-d29LFWFMyINWKX97-Rahc-Yny3g6CMBf3OQOC40lAJXUHVHCcABAGSN',
                        # APP_ID='wx675d68299018008f',
                        # APP_SECRET='5436fb3ceb9fa60cd9685fe70066305b')

        # @robot.handler
        # def hello(message):
            # return 'Hello world'
        # robot.run()
        #endregion
