#encoding=utf-8
import serial #导入模块
import threading
import sys
STRGLO="" #读取的数据
BOOL=True  #读取标志位

#读数代码本体实现
def ReadData(ser):
    global STRGLO,BOOL
    # 循环接收数据，此为死循环，可用线程实现
    while BOOL:
        if ser.in_waiting:
            STRGLO = ser.read(ser.in_waiting)
            print(STRGLO)


#打开串口
# 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
# 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
# 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
def DOpenPort(portx,bps,timeout):
    ret=False
    try:
        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps, timeout=timeout)
        #判断是否打开成功
        if not(ser.is_open):
            ser.open()
        ret=True
        threading.Thread(target=ReadData, args=(ser,)).start()
    except Exception as e:
        print("---Error---：", e)
    return ser,ret



#关闭串口
def DColsePort(ser):
    global BOOL
    BOOL=False
    ser.close()



def WriteData(portx,data,bps = 115200, timeout=None):
    ser = serial.Serial(portx, bps )
    if not(ser.is_open):
            ser.open()
    result = ser.write(data)  # 写数据
    return result
    
#写数据
def DWritePort(ser,text):
    result = ser.write(text)  # 写数据
    return result




#读数据
def DReadPort():
    global STRGLO
    str=STRGLO
    STRGLO=""#清空当次读取
    return str

def GetPorts():
    import serial.tools.list_ports
    try:
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) == 0:
           print('无可用串口')
        else:
            for i in range(0,len(port_list)):
                ser = serial.Serial(port_list[i].device,115200)
                print port_list[i], " IsOpen :",ser.is_open
    except Exception as e:
        print("---Error---：", e)

        
if __name__=="__main__":
    GetPorts()
    portx = "COM1"
    data = "testingdata"
    if len(sys.argv) > 1:
        portx = sys.argv[1]
    if len(sys.argv) > 2:
        data = sys.argv[2]        
    print "write data to port :" , portx ,"\n" , data
    count = WriteData(portx,data)
    print("写入字节数：",count) 
    ser,ret=DOpenPort(portx,115200,None)
    if(ret==True):#判断串口是否成功打开
        if len(sys.argv) > 3 and sys.argv[3]:
            print "read data from port :" , portx
            DReadPort() #读串口数据
        DColsePort(ser)  #关闭串口
