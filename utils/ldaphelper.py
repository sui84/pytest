#encoding=utf-8
import sys
from ldap3 import Server, Connection, SIMPLE, SYNC, ALL, SASL, NTLM,MODIFY_REPLACE

'''

'''
class LdapHelper(object):
    def __init__(self, ldappath ,username , pwd , dcstrs ):
        s = Server(ldappath, get_info=ALL)
        self.c = Connection(s, user=username, password=pwd, authentication=NTLM)
        self.attrs = ['objectClass','sn','cn','samaccountname','mail','mailNickName','title','EmployeeId','userAccountControl','msExchRecipLimit','userPassword']
        self.dcstrs = dcstrs
        
    def ActiveAccount(self,accountctrol):
        account = int ("%s" % accountctrol)
        if (account & 0x0002) > 0:
            return '\tdisabled!\n'
        else:
            return '\tnormal.\n'
        
    def GetDataByAD(self,ad):
        self.c.bind()
        filter='(&(objectClass=user)(sAMAccountName=%s))' % ad
        for dcstr in self.dcstrs:
            self.c.search(dcstr,filter,attributes=self.attrs)
            print len(self.c.entries) , ' record found in ' , dcstr
            for entr in self.c.entries:
                print entr
                print self.ActiveAccount(entr.userAccountControl)
    
    def GetDataByTM(self,tm):
        self.c.bind()
        filter='(&(objectClass=user)(EmployeeId=%s))' % tm
        for dcstr in self.dcstrs:
            self.c.search(dcstr,filter,attributes=self.attrs)
            print len(self.c.entries) , ' record found in ' , dcstr
            for entr in self.c.entries:
                print entr
                print self.ActiveAccount(entr.userAccountControl)

    def GetAttribute(type):
        #type : 'user','person'
        obj=ObjectDef(type,self.c)
        print obj
        

    def GetDNByAD(self,ad):
        connResult = self.c.bind()
        if connResult == True :
            print "Connect successfully!"
        else:
            print "Connect failed!"
        filter='(&(objectClass=user)(sAMAccountName=%s))' % ad
        self.c.search(self.dcstrs,filter,attributes=['cn'])
        print self.c.response
        dnstr = self.c.response[0]['dn']
        return dnstr
    
    def ChangeTMByAD(self,ad,tm):
        # ad : qatminfo01 tm: testtm
        dnstr = self.GetDNByAD(ad)
        result = self.c.modify(dnstr,{'EmployeeId':[(MODIFY_REPLACE,[tm])]})
        if result == True :
            print "successfully!"
        else:
            print "failed!"
    
    def ChangeAttrsByAD(self,ad,attrs):
        dnstr = self.GetDNByAD(ad)
        keys = list(attrs.keys())
        nattrs = {}
        for key in keys:
            nattrs[key] = [(MODIFY_REPLACE,[attrs.get(key)])]
        print nattrs
        result = self.c.modify(dnstr,nattrs)
        if result == True :
            print "successfully!"
        else:
            print "failed!"
    
    def ShowAllAttrs(self):
        #obj=ObjectDef('person',self.c)
        obj=ObjectDef('user',self.c)
        return obj
    
if __name__ == '__main__':
    #disable it :python ldaphelper.py qatminfo01 {'EmployeeId':'testtm','userAccountControl':514}
    #enable it :python ldaphelper.py qatminfo01 {'EmployeeId':'testtm','userAccountControl':512}
    print "AD=%s : Change to %s"  % (sys.argv[1],sys.argv[2])
    attrs=eval(sys.argv[2])
    import yaml
    path=r'D:\temp\test.yaml'
    f=open(path)
    ydata = yaml.load(f)
    ldap , user , pwd ,dcstrs = ydata.get('ldapqa'),ydata.get('qauser'),ydata.get('qapwd'),ydata.get('qadcstr')
    lh = LdapHelper(ldap,user,pwd,dcstrs)
    lh.ChangeAttrsByAD(sys.argv[1],attrs)
    #lh.ChangeTMByAD(sys.argv[1],sys.argv[2])
    '''
    lh = LdapHelper(ldap,user,pwd,dcstrs)
    lh.GetDataByAD('testad')
    #lh.GetDataByTM('12345')
    '''
