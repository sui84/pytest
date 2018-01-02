#coding=utf-8
import jpype
import os



class JT400Helper(object):
    def __init__(self, server,username,pwd):
        jvmpath=r"C:\Program Files\Java\jre1.8.0_60\bin\server\jvm.dll"
        jarpath=r'd:\temp\jt400.jar'
        jvmArg = "-Djava.class.path=%s" % jarpath
        jpype.startJVM(jvmpath,jvmArg)
        
        #jt400
        AS400=jpype.JClass('com.ibm.as400.access.AS400')
        CommandCall=jpype.JClass('com.ibm.as400.access.CommandCall')
        ProgramCall=jpype.JClass('com.ibm.as400.access.ProgramCall')
        SpooledFileList=jpype.JClass('com.ibm.as400.access.SpooledFileList')
        AS400Text=jpype.JClass('com.ibm.as400.access.AS400Text')
        AS400JDBCDriver=jpype.JClass('com.ibm.as400.access.AS400JDBCDriver')
        
        
        
        #java
        Connection=jpype.JClass('java.sql.Connection')
        DatabaseMetaData=jpype.JClass('java.sql.DatabaseMetaData')
        Statement=jpype.JClass('java.sql.Statement')
        self.ResultSet=jpype.JClass('java.sql.ResultSet')
        
        self.server,self.username,self.pwd = server,username,pwd
        self.RJobLog=jpype.JClass('com.ibm.as400.resource.RJobLog')
        self.AS400FTP=jpype.JClass('com.ibm.as400.access.AS400FTP')
        self.IFSFile=jpype.JClass('com.ibm.as400.access.IFSFile')
        
        self.ProgramParameter=jpype.JClass('com.ibm.as400.access.ProgramParameter')
        self.DriverManager=jpype.JClass('java.sql.DriverManager')
        self.DriverManager.registerDriver(AS400JDBCDriver())
        
        
        self.system=AS400(server,username,pwd)
        self.cc=CommandCall(self.system)
        self.outqueue = SpooledFileList(self.system)
        self.pc = ProgramCall(self.system)
    
    def ShowIfs(self,ifspath):
        ifs=self.IFSFile(self.system,ifspath)
        print 'exists : ',ifs.exists()
        print 'isDirectory : ',ifs.isDirectory()
        print 'isFile : ',ifs.isFile()
        fs=ifs.listFiles()
        if len(fs)>0:
            for f in fs:
                print f.name
        
    
    def SaveFieldDef(self,flib,file,tmplib,ofile):
        cmdstr = "DSPFFD FILE(%s/%s) OUTPUT(*OUTFILE) OUTFILE(%s/FIELDDEF)" % (flib,file,tmplib)
        msg = self.GetCmdMsg(cmdstr)
        if msg == "":
            cmdstr = "SELECT WHFLDI, WHFTXT, WHFLDT, WHFLDD, WHFLDP,WHFLDB, WHFOBO FROM %s.FIELDDEF WHERE WHFLDI <> ' ' ORDER BY WHFOBO" % tmplib
            self.SaveSQLResult(cmdstr,ofile)
    
    def SaveJobLog(self,jobstr,ofile):
        msg = self.GetJobLog(jobstr)
        with open(ofile,'w') as f:
            f.write(msg)
    
    def GetJobLog(self,jobstr):
        jobarr = jobstr.split('/')
        jobnum,jobuser,jobname=jobarr[0],jobarr[1],jobarr[2]
        return self.GetJobLogByNum(jobnum,jobuser,jobname)
        
    def GetJobLogByNum(self,jobnum,jobuser,jobname):
        joblog=self.RJobLog(self.system,jobname,jobuser,jobnum)
        joblog.open()
        joblog.waitForComplete()
        num=joblog.getListLength()
        msgs = []
        for i in range(0,num):
            qmsg=joblog.resourceAt(i)
            msgs.append(qmsg.getAttributeValue("MESSAGE_TEXT"))
        msg = '\n'.join(msgs)
        return msg
    
    
    def SaveSQLResult(self,cmdstr,ofile):
        connection = self.DriverManager.getConnection("jdbc:as400://" + self.server, self.username, self.pwd)
        dmd = connection.getMetaData()
        select = connection.createStatement(self.ResultSet.TYPE_SCROLL_SENSITIVE,self.ResultSet.CONCUR_UPDATABLE)
        print cmdstr
        rs = select.executeQuery(cmdstr)
        strs = ""
        cols = rs.getMetaData().getColumnCount()
        while (rs.next()):
            rowstrs = []
            for i in range(1,cols+1):
                value = rs.getString(i)
                if ' ' in value:
                    value = '"%s"' % value
                rowstrs.append(rs.getString(i))
            strs+=','.join(rowstrs)+'\n'
        with open(ofile,'w') as f:
            f.write(strs)
        connection.close();
     
    def CallProgram(self,plib,pgm,paras):
        #WRKACTJOB SBS(QUSRWRK) JOB(QZRCSRVS) - dump not work
        #paras=["Y","12345","      "]    
        pgmparas=[]
        for para in paras:
            pgmparas.append(ProgramParameter(para))
            print str(pgmparas.getInputData())
        self.pc.setProgram("/QSYS.LIB/%s.LIB/%s.PGM" % (plib,pgm),pgmparas)
        successfully = self.pc.run()
        msg = ''
        job = pc.getJob()
        print pc.toString()
        print job.toString()
        if successfully <> True:
            ml=self.pc.getMessageList()
            for m in ml:
                msg += m.getText() +'\n'
            print msg
            self.system.disconnectAllServices()
        return msg
        
    def GetCmdMsg(self,cmdstr):
        msg = ''
        print cmdstr
        successfully = self.cc.run(cmdstr)
        if successfully <> True:
            ml=self.cc.getMessageList()
            for m in ml:
                msg += m.getText() +'\n'
            print msg
        return msg
    
    def CheckObjExists(self,lib,file,type="*FILE"):
        str = "CHKOBJ OBJ(%s/%s) OBJTYPE(%s)" % (lib,file,type)
        return self.GetCmdMsg(str)

    def DeleteObj(self,lib,file):    
        str = "DLTF FILE(%s/%s)" % (lib,file)
        return self.GetCmdMsg(str)
        
        
    def FileToIfs(self,lib,file,mem,ifspath):
        # don't use RMVBLANK(*TRAILING) ,will cause numeric field contains blank characters error when put ifs to file
        str = "CPYTOIMPF FROMFILE(%s/%s %s) TOSTMF('%s') MBROPT(*REPLACE) STMFCCSID(*STMF) RCDDLM(*CRLF) DTAFMT(*DLM) STRDLM(*NONE)" % (lib,file,mem,ifspath)
        print lib,file,mem,"->",ifspath
        return self.GetCmdMsg(str)
        
    def IfsToFile(self,ifspath,lib,file,mem):
        str = "CPYFRMIMPF FROMSTMF('%s') TOFILE(%s/%s %s) MBROPT(*REPLACE) RCDDLM(*CRLF) STRDLM(*NONE) FLDDLM(',') ERRRCDOPT(*REPLACE) RPLNULLVAL(*FLDDFT)" % (ifspath,lib,file,mem)
        print ifspath,"->",lib,file,mem
        return self.GetCmdMsg(str)
        
    def FileToPc(self,lib,file,mem,ofile):
        tmpifs = "QDLS/TEMP/%s.CSV" % mem
        self.FileToIfs(lib,file,mem,tmpifs)
        self.FtpGetIfsFile(tmpifs,ofile)
    
    def PcToFile(self,ifile,lib,file,mem):
        tmpifs = "QDLS/TEMP/%s.CSV" % mem
        self.FtpPutIfsFile(ifile,tmpifs)
        self.IfsToFile(tmpifs,lib,file,mem)
        

    def FtpGetIfsFile(self,ifspath,ofile):
        ftp=self.AS400FTP(self.system)
        successfully = ftp.get(ifspath,ofile)
        print ifspath,"->",ofile
        return successfully
        
    def FtpGetText(self,lib,srcf,mem,dest=r"d:\temp"):
        ftp=self.AS400FTP(self.system)
        target="/QSYS.LIB/%s.LIB/%s.FILE/%s.MBR" % (lib,srcf,mem)
        if os.path.isdir(dest):
            dest=os.path.join(dest,mem+".txt")
        print target,"->",dest
        successfully = ftp.get(target,dest)
        return successfully
        
    def FtpGetSavf(self,lib,savf,dest=r"d:\temp"):
        ftp=self.AS400FTP(self.system)
        target="/QSYS.LIB/%s.LIB/%s.SAVF" % (lib,savf)
        # QUOTE SITE NAMEFMT 0 QGPL/QCLSRC.TEST
        # QUOTE SITE NAMEFMT 1 /QSYS.lib/Libname.lib/Fname.file/Mname.mbr
        ftp.issueCommand("quote site namefmt 1")
        if os.path.isdir(dest):
            dest=os.path.join(dest,savf+".SAVF")
        # can not get it if not set data transfer type
        ftp.setDataTransferType(1)
        successfully = ftp.get(target,dest)
        return successfully
     
    
    def FtpPutIfsFile(self,ifile,ifspath):
        ftp=self.AS400FTP(self.system)
        successfully = ftp.put(ifile,ifspath)
        print ifile,"->",ifspath
        return successfully
             
    def FtpPutText(self,ifile,lib,srcf,mem):
        ftp=self.AS400FTP(self.system)
        dest="/QSYS.LIB/%s.LIB/%s.FILE/%s.MBR" % (lib,srcf,mem)
        successfully = ftp.put(ifile,dest)
        print ifile,"->",lib,srcf,mem
        return successfully
    
    def GetOutQList(self,outqlib,outq):
        print "OutQueue : %s/%s" % (outqlib,outq)
        self.outqueue.setQueueFilter("/QSYS.LIB/%s.LIB/%s.OUTQ" % (outqlib,outq))
        self.outqueue.setUserFilter("*ALL")
        self.outqueue.openSynchronously()
        enums=self.outqueue.getObjects()
        i = 1
        info = ""
        while (enums.hasMoreElements()):
            splf=enums.nextElement()
            if(splf<>None):
                strs=[]
                strs.append("System :%s , File : %s , File Number : %s , Progarm :%s , Date : %s" % (splf.getStringAttribute(271),splf.getStringAttribute(104),splf.getIntegerAttribute(105).toString(),splf.getStringAttribute(272),splf.getStringAttribute(34)))
                strs.append("Number/User/Job : %s/%s/%s" % (splf.getStringAttribute(60),splf.getStringAttribute(62),splf.getStringAttribute(59)))
                strs.append("File Pages: %s , Print quality : %s , Printer device type : %s , Page size length : %d " % (splf.getIntegerAttribute(111).toString(),splf.getStringAttribute(48),splf.getStringAttribute(90),splf.getFloatAttribute(78).intValue()))
                info += '\n'.join(strs)+'\n'
                i+=1
        self.system.disconnectAllServices()
        print "total spool files : ",i
        print info
    
    def GetSpoolFile(self,sflib,sffile,sfname,sfjobnum,fnum,dest):
        if self.CheckObjExists(sflib,sffile)<>"":
            # IGCDTA parameter is for DBCS file
            self.GetCmdMsg("CRTPF FILE(%s/%s) RCDLEN(160) IGCDTA(*YES)" % (sflib,sffile))
        str = "CPYSPLF FILE(%s) TOFILE(%s/%s) JOB(%s) SPLNBR(%d)" % (sfname,sflib,sffile,sfjobnum,fnum)
        msg = self.GetCmdMsg(str)
        if msg == "":
            self.FtpGetText(sflib,sffile,sffile,dest)
            print "download successfully!"
    
        
if __name__ == '__main__':
    pass
