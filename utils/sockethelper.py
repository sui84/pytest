#coding=utf-8
import socket
import os

class SocketHelper(object):
    def __init__(self):
        pass

    def GetIPForHost(self,hostname="www.google.com"):
        ip = socket.gethostbyname(hostname)
        return ip

    def GetDns(self,hostname="www.google.com"):
        dns = socket.getaddrinfo(hostname,80)
        return dns

    def StartServer(self,hostname='localhost',port=8081):
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #从指定的端口，从任何发送者，接收UDP数据
        s.bind((hostname,port))
        print(u'正在等待接入...')
        while True:
            #接收一个数据
            data,addr=s.recvfrom(1024)
            print(u'Received:',data,u'from',addr)

    def StartClient(self,hostname='localhost',port=8081,data="hello,world!"):
        port=8081
        host='localhost'
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.sendto(data,(host,port))


if __name__ == '__main__':
    s = SocketHelper()
    s.StartServer()
    #s.StartClient(data=u"你好,testing".encode('utf-8')
