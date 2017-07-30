#encoding=utf-8
import re
'''
http://www.cnblogs.com/deerchao/archive/2006/08/24/zhengzhe30fengzhongjiaocheng.html
\d 数字
\w 字母数字和下划线
\t 制表符
. 除了回车以外的所有字符
+ >=1
* >=0
? 0 or 1
{m} m次
{m,n} between m and n
'''


class RegHelper(object):
    def __init__(self):
        numcom = re.compile('\d+')

    def NumMatch(self,str):
        #只从开始找
        #result = re.match('\d+',str)
        result = self.numcom.match(str)
        if result:
            print result.group()
        else:
            print 'nothing'
        return result.group()

    def NumMatch(self,str):
        result = re.search('\d+',str)
        if result:
            print result.group()
        else:
            print 'nothing'
        return result.group()

    def GetAllNumMatch(self,str):
        result = re.findall('\d+',str)
        if result:
            print result
        else:
            print 'nothing'
        return result

