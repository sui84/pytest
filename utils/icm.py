import itchatmp

itchatmp.config(itchatmp.WechatConfig(
    token='bUiy1ZwNDNBSIRIxOGPqpojOc9JIcfGRMAs8J1Ww9xyL6Z8nyz9cLdNDnSfuW-3x_Oy2E3ZGYARjo8QqHl-d29LFWFMyINWKX97-Rahc-Yny3g6CMBf3OQOC40lAJXUHVHCcABAGSN',
    appId = 'wx675d68299018008f',
    appSecret = '5436fb3ceb9fa60cd9685fe70066305b'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    return msg['Content']

itchatmp.run()