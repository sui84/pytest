#encoding=utf-8
from scapy.all import *
import logging
from enum import Enum
import time
import fhelper
import confhelper
import threadhelper
import threading
from timehelper import elapsedtimedeco


#region TCP Flags
'''
* F = 0x0001: FIN - 结束; 结束会话
* S = 0x0002: SYN - 同步; 表示开始会话请求
* R = 0x0004: RST - 复位;中断一个连接
* P = 0x0008: PUSH - 推送; 数据包立即发送
* A = 0x0010: ACK - 应答
* U = 0x0020: URG - 紧急
* E = 0x0040: ECE - 显式拥塞提醒回应
* W = 0x0080: CWR - 拥塞窗口减少

'''
#endregion
#region ICMP Types
'''
TYPE	CODE	Description	Query	Error
0	0	Echo Reply——回显应答（Ping应答）	x
3	0	Network Unreachable——网络不可达	 	x
3	1	Host Unreachable——主机不可达	 	x
3	2	Protocol Unreachable——协议不可达	 	x
3	3	Port Unreachable——端口不可达	 	x
3	4	Fragmentation needed but no frag. bit set——需要进行分片但设置不分片比特	 	x
3	5	Source routing failed——源站选路失败	 	x
3	6	Destination network unknown——目的网络未知	 	x
3	7	Destination host unknown——目的主机未知	 	x
3	8	Source host isolated (obsolete)——源主机被隔离（作废不用）	 	x
3	9	Destination network administratively prohibited——目的网络被强制禁止	 	x
3	10	Destination host administratively prohibited——目的主机被强制禁止	 	x
3	11	Network unreachable for TOS——由于服务类型TOS，网络不可达	 	x
3	12	Host unreachable for TOS——由于服务类型TOS，主机不可达	 	x
3	13	Communication administratively prohibited by filtering——由于过滤，通信被强制禁止	 	x
3	14	Host precedence violation——主机越权	 	x
3	15	Precedence cutoff in effect——优先中止生效	 	x
4	0	Source quench——源端被关闭（基本流控制）
5	0	Redirect for network——对网络重定向
5	1	Redirect for host——对主机重定向
5	2	Redirect for TOS and network——对服务类型和网络重定向
5	3	Redirect for TOS and host——对服务类型和主机重定向
8	0	Echo request——回显请求（Ping请求）	x
9	0	Router advertisement——路由器通告
10	0	Route solicitation——路由器请求
11	0	TTL equals 0 during transit——传输期间生存时间为0	 	x
11	1	TTL equals 0 during reassembly——在数据报组装期间生存时间为0	 	x
12	0	IP header bad (catchall error)——坏的IP首部（包括各种差错）	 	x
12	1	Required options missing——缺少必需的选项	 	x
13	0	Timestamp request (obsolete)——时间戳请求（作废不用）	x
14	 	Timestamp reply (obsolete)——时间戳应答（作废不用）	x
15	0	Information request (obsolete)——信息请求（作废不用）	x
16	0	Information reply (obsolete)——信息应答（作废不用）	x
17	0	Address mask request——地址掩码请求	x
18	0	Address mask reply——地址掩码应答
posted on 2009-06-24 12:37 可冉 阅读(15082) 评论(0)  编辑 收藏 引用 所属分类: cisco 、协议 、系统 、linux'''
#endregion

class ScapyHelper(object):
    def __init__(self,outfile=r"..\out\scanports.txt"):
        self.confile = r"..\conf\test.conf"
        self.dst_ip = "192.168.1.1"
        self.src_port = RandShort()
        self.dst_port=80
        self.dst_timeout=10
        self.outfile=outfile
        self.openstatus = 'Open'
        self.closedstatus = 'Closed'
        self.filteredstatus = 'Filtered'
        self.unknowstatus = 'Unknow'
        #self.mu = threading.Lock() #1、创建一个锁
        self.portscans = []
        logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

        #self.ScanTCPAck(self.dst_ip,self.src_port,self.dst_port)
        #self.ScanTCPWindowsize(self.dst_ip,self.src_port,self.dst_port)

        #failed
        #self.ScanTCPXmas(self.dst_ip,self.src_port,self.dst_port)
        #self.udp_scan(self.dst_ip,self.src_port,self.dst_port)
        #self.ScanTCPFin(self.dst_ip,self.src_port,self.dst_port)
        #self.ScanTCPNull(self.dst_ip,self.src_port,self.dst_port)
    def OutputFile(self,portscan,outfile):
        f=fhelper.FHelper(outfile)
        f.SaveDictList(portscan)

    def ScanPortRange(self,ips,portstart=0,portend=1024):
        portscan = self.ScanPorts(ips,range(portstart,portend))
        return portscan


    def GetPorts(self):
        conf =  confhelper.ConfHelper(self.confile)
        scanports = conf.GetSectionConfig("scanports")
        if scanports.has_key("ips"):
            ips=scanports.get("ips").split(',')
        if scanports.has_key("ports"):
            ports=scanports.get("ports").split(',')
            ports=[int(item) for item in ports]
        return ips,ports

    @elapsedtimedeco(True)
    def MultiProcessScanPorts(self):
        t=threadhelper.ThreadHelper()
        #sh.ScanTCP('192.168.1.1',RandShort(),80)
        #portscans = sh.ScanTCP('192.168.1.1',RandShort
        #portscans = sh.ScanPorts(ips=[],ports=[])
        args=[]
        ips,ports = self.GetPorts()
        for ip in ips:
            for port in ports:
                args.append((ip,RandShort(),port))
        t.MultiThreadExecute(self.WrapperScanPorts,args)

    def WrapperScanPorts(self,args):
        #多个参数用这层包起来
        return self.ScanTCP(*args)

    # 调用计时装饰器
    # 装饰器使得线程共享变量失效，存不到数据
    @elapsedtimedeco(True)
    def ScanPorts(self,ips=[],ports=[]):
        self.portscans = []
        if len(ips)==0 and len(ports)==0:
            ips,ports = self.GetPorts()
        data=[]
        for ip in ips:
            for port in ports:
                data.append(((ip,self.src_port,port), None))
                #status=self.ScanTCP(ip,self.src_port,port)
                #portscans.append({"dst_ip":ip,"dst_port":port,"status":status})

        t = threadhelper.ThreadHelper()
        t.WorkWithMultipleThreads(self.ScanTCP,data)
        return self.portscans

    def CheckICMP(self,stealth_scan_resp):
        if(int(stealth_scan_resp.getlayer(ICMP).type)==3 and int(stealth_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
            return 1

    def ScanTCP(self,dst_ip,src_port,dst_port):
    #1. TCP 连接扫描 # 2.TCP SYN 扫描
    # open
    #(B) --> [SYN] --> (A)
    #(B) <-- [SYN/ACK] <--(A)
    #(B) --> [RST/ACK] --> (A) , (B) --> [RST] --> (A)
    # close
    #(B) --> [SYN] --> (A)
    #(B) <-- [RST] <--(A)
        stealth_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=10)
        status = self.unknowstatus
        if stealth_scan_resp <> None:
            if(str(type(stealth_scan_resp))==""):
                status = self.filteredstatus
            elif(stealth_scan_resp.haslayer(TCP)):
                if(stealth_scan_resp.getlayer(TCP).flags == 0x12):
                    send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="R"),timeout=10)
                    #send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="AR"),timeout=10)
                    status = self.openstatus
                elif (stealth_scan_resp.getlayer(TCP).flags == 0x14):
                    status = self.closedstatus
            elif(stealth_scan_resp.haslayer(ICMP)):
                if self.CheckICMP(stealth_scan_resp):
                    status = self.filteredstatus

        print "IP:",dst_ip,"Port:",dst_port,"Status:",status
        '''
        if self.mu.acquire(True): #2、获取锁状态，一个线程有锁时，别的线程只能在外面等着
            self.portscans.append({"dst_ip":dst_ip,"dst_port":dst_port,"status":status})
            self.mu.release() #3、释放锁
       '''
        with open(self.outfile,'a') as f:
            f.write("IP: %s,Port: %d,Status: %s\n" % (dst_ip,dst_port,status))
        return status

    # 利用协程可以return data后再一起保存
    @elapsedtimedeco(True)
    def GetScanPorts(self,ips=[],ports=[]):
        self.portscans = []
        if len(ips)==0 and len(ports)==0:
            ips,ports = self.GetPorts()
        data=[]
        for ip in ips:
            for port in ports:
                data.append((ip,self.src_port,port))
                #status=self.ScanTCP(ip,self.src_port,port)
                #portscans.append({"dst_ip":ip,"dst_port":port,"status":status})

        t = threadhelper.ThreadHelper()
        result =  t.MultiGEventExecute(self.WrapperGetScanPorts,data)
        print result
        with open(self.outfile,'a') as f:
            f.writelines(result)
        return self.portscans

    def WrapperGetScanPorts(self,args):
        #多个参数用这层包起来
        return self.GetScanTCP(*args)

    def GetScanTCP(self,dst_ip,src_port,dst_port):
        stealth_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=10)
        status = self.unknowstatus
        if stealth_scan_resp <> None:
            if(str(type(stealth_scan_resp))==""):
                status = self.filteredstatus
            elif(stealth_scan_resp.haslayer(TCP)):
                if(stealth_scan_resp.getlayer(TCP).flags == 0x12):
                    send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="R"),timeout=10)
                    #send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="AR"),timeout=10)
                    status = self.openstatus
                elif (stealth_scan_resp.getlayer(TCP).flags == 0x14):
                    status = self.closedstatus
            elif(stealth_scan_resp.haslayer(ICMP)):
                if self.CheckICMP(stealth_scan_resp):
                    status = self.filteredstatus
        result = "IP: %s,Port: %d,Status: %s\n" % (dst_ip,dst_port,status)
        return result

    def ScanTCPXmas(self,dst_ip,src_port,dst_port):
    #3.TCP 圣诞树(Xmas Tree)扫描 ！失败 slow, xmas_scan_resp NoneType
    # open
    #(B) --> [PSH,FIN,URG] --> (A)
    #(B) <--  None <--(A)
    # close
    #(B) --> [PSH,FIN,URG] --> (A)
    #(B) <--  [RST] <--(A)
    # filter
    #(B) --> [PSH,FIN,URG] --> (A)
    #(B) <-- ICMP Error (type 3 , code 1，2，3，9，10或13 )<--(A)
        xmas_scan_resp = sr1(IP(dst=dst_ip)/TCP(dport=dst_port,flags="FPU"),timeout=10)
        if (str(type(xmas_scan_resp))==""):
            print "Open|Filtered"
        elif(xmas_scan_resp.haslayer(TCP)):
            if(xmas_scan_resp.getlayer(TCP).flags == 0x14):
                print "Closed"
        elif(xmas_scan_resp.haslayer(ICMP)):
            if self.CheckICMP(xmas_scan_resp):
                print "Filtered"


        #4. TCP FIN扫描 ! 失败  fin_scan_resp NoneType
    # open
    #(B) --> [FIN] --> (A)
    #(B) <--  None <--(A)
    # close
    #(B) --> [FIN] --> (A)
    #(B) <--  [RST] <--(A)
    # filter
    #(B) --> [FIN] --> (A)
    #(B) <-- ICMP Error (type 3 , code 1，2，3，9，10或13 )<--(A)
    def ScanTCPFin(self,dst_ip,src_port,dst_port):
        fin_scan_resp = sr1(IP(dst=dst_ip)/TCP(dport=dst_port,flags="F"),timeout=10)
        if (str(type(fin_scan_resp))==""):
            print "Open|Filtered"
        elif(fin_scan_resp.haslayer(TCP)):
            if(fin_scan_resp.getlayer(TCP).flags == 0x14):
                print "Closed"
        elif(fin_scan_resp.haslayer(ICMP)):
            if self.CheckICMP(fin_scan_resp):
                print "Filtered"



    #5.TCP 空扫描(Null) ! 失败  fin_scan_resp NoneType
    # open
    #(B) --> [] --> (A)
    #(B) <--  None <--(A)
    # close
    #(B) --> [] --> (A)
    #(B) <--  [RST] <--(A)
    # filter
    #(B) --> [] --> (A)
    #(B) <-- ICMP Error (type 3 , code 1，2，3，9，10或13 )<--(A)
    def ScanTCPNull(self,dst_ip,src_port,dst_port):
        null_scan_resp = sr1(IP(dst=dst_ip)/TCP(dport=dst_port,flags=""),timeout=10)
        if (str(type(null_scan_resp))==""):
            print "Open|Filtered"
        elif(null_scan_resp.haslayer(TCP)):
            if(null_scan_resp.getlayer(TCP).flags == 0x14):
                print "Closed"
        elif(null_scan_resp.haslayer(ICMP)):
            if(int(null_scan_resp.getlayer(ICMP).type)==3 and int(null_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                print "Filtered"

    #6.TCP ACK扫描
    # not filter
    #(B) --> [ACK] --> (A)
    #(B) <--  [RST] <--(A)
    # filter
    #(B) --> [ACK] --> (A)
    #(B) <-- ICMP Error (type 3 , code 1，2，3，9，10或13 )<--(A)
    def ScanTCPAck(self,dst_ip,src_port,dst_port):
        ack_flag_scan_resp = sr1(IP(dst=dst_ip)/TCP(dport=dst_port,flags="A"),timeout=10)
        if (str(type(ack_flag_scan_resp))==""):
            print "Stateful firewall presentn(Filtered)"
        elif(ack_flag_scan_resp.haslayer(TCP)):
            if(ack_flag_scan_resp.getlayer(TCP).flags == 0x4):
                print "No firewalln(Unfiltered)"
        elif(ack_flag_scan_resp.haslayer(ICMP)):
            if(int(ack_flag_scan_resp.getlayer(ICMP).type)==3 and int(ack_flag_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                print "Stateful firewall presentn(Filtered)"

    #7.TCP窗口扫描
         # open
    #(B) --> [ACK] --> (A)
    #(B) <--  [RST with positive window size] <--(A)
    # close
    #(B) --> [ACK] --> (A)
    #(B) <--  [RST with 0 window size] <--(A)
    def ScanTCPWindowsize(self,dst_ip,src_port,dst_port):
        window_scan_resp = sr1(IP(dst=dst_ip)/TCP(dport=dst_port,flags="A"),timeout=10)
        if (str(type(window_scan_resp))==""):
            print "No response"
        elif(window_scan_resp.haslayer(TCP)):
            if(window_scan_resp.getlayer(TCP).window == 0):
                print "Closed"
            elif(window_scan_resp.getlayer(TCP).window > 0):
                print "Open"

    #8.UDP扫描  ！失败 udp_scan_resp <class 'scapy.layers.inet.IP'>
     # open
    #(B) --> UDP package --> (A)
    #(B) <--  UDP package <--(A)

     # close
    #(B) --> UDP package --> (A)
    #(B) <-- ICMP Error (type 3 , code 3)<--(A)
    # filter
    #(B) --> UDP package --> (A)
    #(B) <-- ICMP Error (type 3 , code 1，2，3，9，10或13 )<--(A)
            # open/filter
    #(B) --> UDP package--> (A)
    #(B) <--  None <--(A)
    def udp_scan(self,dst_ip,dst_port,dst_timeout):
        udp_scan_resp = sr1(IP(dst=dst_ip)/UDP(dport=dst_port),timeout=dst_timeout)
        print type(udp_scan_resp)
        if (str(type(udp_scan_resp))==""):
            retrans = []
            for count in range(0,3):
                retrans.append(sr1(IP(dst=dst_ip)/UDP(dport=dst_port),timeout=dst_timeout))
            for item in retrans:
                if (str(type(item))!=""):
                    udp_scan(dst_ip,dst_port,dst_timeout)
            return "Open|Filtered"
        elif (udp_scan_resp.haslayer(UDP)):
            return "Open"
        elif(udp_scan_resp.haslayer(ICMP)):
            if(int(udp_scan_resp.getlayer(ICMP).type)==3 and int(udp_scan_resp.getlayer(ICMP).code)==3):
                return "Closed"
            elif(int(udp_scan_resp.getlayer(ICMP).type)==3 and int(udp_scan_resp.getlayer(ICMP).code) in [1,2,9,10,13]):
                return "Filtered"

if __name__ == '__main__':
    sh = ScapyHelper()
    #sh.MultiProcessScanPorts()
    #sh.ScanTCP('192.168.1.1',RandShort(),80)
    #portscans = sh.ScanTCP('192.168.1.1',RandShort
    # 多进程速度最快
    portscans = sh.ScanPorts(ips=[],ports=[])
    #协程调用，比多进程多花了好几倍时间
    #portscans =sh.GetScanPorts(ips=[],ports=[])






