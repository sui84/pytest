#encoding=utf-8
import psutil
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import platform

def computer():
    #查看cpu的信息
    print u"CPU 个数 %s"%psutil.cpu_count()
    print u"物理CPU个数 %s"%psutil.cpu_count(logical=False)
    print u"CPU uptimes"
    print psutil.cpu_times()
    print ""

    #查看内存信息
    mem = psutil.virtual_memory()
    print u"系统总内存 %s G"%(mem.total/1024/1024/1024)
    print u"系统可用内存 %s G"%(mem.available/1024/1024/1024)
    mem_rate = int(mem.available)/float(mem.total)
    print u"系统内存使用率 %s %%"%int(mem_rate*100)

    #交换分区
    swapmem = psutil.swap_memory()
    print u"交换分区 %s G"%(swapmem.total/1024/1024/1024)
    print u"交换分区可用 %s G"%(swapmem.free/1024/1024/1024)
    print u"交换分区使用率 %s %%"%int(swapmem.percent)
    #系统启动时间
    print u"系统启动时间 %s"%datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    #系统用户
    users_count = len(psutil.users())
    users_list = ",".join([ u.name for u in psutil.users()])
    print u"当前有%s个用户，分别是%s"%(users_count, users_list)

    #网卡，可以得到网卡属性，连接数，当前流量等信息
    net = psutil.net_io_counters()
    bytes_sent = '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024)
    bytes_rcvd = '{0:.2f} Mb'.format(net.bytes_sent / 1024 / 1024)
    print u"网卡接收流量 %s 网卡发送流量 %s"%(bytes_rcvd, bytes_sent)
    nis=psutil.net_io_counters(pernic=True)
    print u"网卡 " ,tuple(nis)

    '''
    pids=psutil.pids()
    for pid in pids:
        show_process(pid)
    '''
    with open (r'd:\temp\test.txt','w') as f:
        __console__=sys.stdout
        sys.stdout=f
        for proc in psutil.process_iter():
            '''
            if proc.name() == "w3wp.exe":
                cpu_threshold=proc.cpu_percent(interval=2)/24
                print proc.name(),proc.create_time(),cpu_threshold
                p.terminate() proc .kill()
                Iterate over all ports this process is listening to
            for con in proc.get_connections():
                con
            '''
            pa=proc.as_dict()
            print pa.get('name'),pa.get('create_time'),pa.get('pid'),pa.get('status'),pa.get('connections'),pa.get('open_files'),pa.get('cpu_percent'),pa.get('memory_percent'),pa.get('username'),pa.get('num_threads')

        print u"当前进程:",psutil.Process(os.getpid()).cmdline()
        sys.stdout=__console__

    #磁盘 磁盘的使用量等等
    dps=psutil.disk_partitions()
    for dp in dps:
        dp
    du=psutil.disk_usage('/')
    print "Disk total %s G"%(du.total/1024/1024/1024)
    print "Disk avaiable %s G"%(du.free/1024/1024/1024)
    print "Disk use %s %%"%(du.percent)

    print platform.system() #获取操作系统环境
    print platform.platform() #获取操作系统名称及版本号
    print platform.version() #获取操作系统版本号
    print platform.architecture()#获取操作系统的位数
    print platform.machine()#计算机类型
    print platform.node() #计算机的网络名称
    print platform.processor() #计算机处理器信息

#进程  进程的各种详细参数
def show_process(pid):
    try:
        p = psutil.Process(pid)

        p.name()   #进程名
        #p.exe()    #进程的bin路径
        #p.cwd()    #进程的工作目录绝对路径
        p.status()   #进程状态
        p.create_time()  #进程创建时间
        #p.uids()    #进程uid信息
        #p.gids()    #进程的gid信息
        p.cpu_times()   #进程的cpu时间信息,包括user,system两个cpu信息
        #p.cpu_affinity()  #get进程cpu亲和度,如果要设置cpu亲和度,将cpu号作为参考就好
        p.memory_percent()  #进程内存利用率
        p.memory_info()    #进程内存rss,vms信息
        p.io_counters()    #进程的IO信息,包括读写IO数字及参数
        #p.connectios()   #返回进程列表
        p.num_threads()  #进程开启的线程数
        '''
        听过psutil的Popen方法启动应用程序，可以跟踪程序的相关信息
        from subprocess import PIPE
        p = psutil.Popen(["/usr/bin/python", "-c", "print('hello')"],stdout=PIPE)
        '''
        p.name()
        #p.username()
    except:
        pass

if __name__ == '__main__':
    computer()
