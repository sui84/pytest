#coding=utf-8
import socket

class SocketHelper(object):
    def __init__(self):
        pass

    def GetIPForHost(self,hostname="www.google.com"):
        ip = socket.gethostbyname(hostname)
        return ip

    def GetDns(self,hostname="www.google.com"):
        dns = socket.getaddrinfo(hostname,80)
        return dns


if __name__ == '__main__':
    pass
