import socket, sys, threading
from p2logic import *
from queue import Queue
import time

#Thanks Professor Austin for teaching me queue
#it has to be global.
mouseClickQueue = Queue()
recvQueue = Queue()

#Code studied from http://t.csdn.cn/zAQYq, modified.

def startClient(app):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6666))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    t = threading.Thread(target=constantRecv, args=(s,))
    t.start()
    t2 = threading.Thread(target=constantSend,args = (s,))
    t2.start()
 
def constantRecv(s):
    while True:
        data = s.recv(1024)
        info = data.decode().split(',')
        recvQueue.put(info)

def constantSend(s):
    while True:
        r,c = mouseClickQueue.get()
        info = str(r) + ',' + str(c)
        data = info.encode()
        s.send(data)

