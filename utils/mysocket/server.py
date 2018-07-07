#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import socket

Server_IP = '127.0.0.1'
Server_Port = 7777
Buf_Size = 1024

def main():
    #创建套接字
    serSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    localAddr = (Server_IP,Server_Port)
    serSocket.bind(localAddr)
    # 设置一个套接字属性；
    serSocket.setblocking(False)

    serSocket.listen(5)
    # 用来保存所有连接的客户单

    serSocketList = []
    while True:
        # 等待新的一个客户端的到来
        # newSocket,destAddr = serSocket.accept()
        try:
            newSocket,clientAddr = serSocket.accept()
            newSocket.setblocking(False)

            serSocketList.append((newSocket,clientAddr))
        except:
            pass
        else:
            print u'一个新的客户端到来',clientAddr


        for newSocketj,clientAddr in serSocketList:
            try:
               recvData= newSocket.recv(Buf_Size)
            except:
                pass
            else:
                if len(recvData):
                    print('%s:%s'%(str(clientAddr),recvData))
                    newSocket.send('[%s] %s' % ("You send:", recvData))    # 给客户端发送信息

                else:
                    newSocket.close()
                    serSocketList.remove((newSocket,clientAddr))
                    print('%s:已经下线'%(str(clientAddr)))



if __name__ == '__main__':
    main()
