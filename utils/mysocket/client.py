#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import server
from socket import *

host = server.Server_IP
port = server.Server_Port
bufsiz = server.Buf_Size


def main():
    tcpCliSock = socket(AF_INET, SOCK_STREAM)    # 开启套接字
    tcpCliSock.connect((host, port))             # 连接到服务器

    while True:
        data = raw_input('> ')      # 等待输入
        if not data:
            break
        tcpCliSock.send(data)       # 发送信息
        response = tcpCliSock.recv(bufsiz)       # 接受返回信息
        if not response:
            break
        print response

    tcpCliSock.close()

if __name__ == '__main__':
    main()
