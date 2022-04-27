import socket, threading, sys, time
from  bomb import *
from queue import Queue

#Thanks Professor Austin for teaching me queue
#it has to be global.
sendQueue = Queue()
recvQueue = Queue()

#Code studied from http://t.csdn.cn/zAQYq, modified.

def startServer(app):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #This is for local connection. Change to IP address for other connections
        s.bind(('127.0.0.1', 6666))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting for connection...')
    print('')

    app.currRow, app.currCol = None,None
    app.currLock = None
    app.p2Play = False
    app.connected = False

    threading.Thread(target = connectClient, args = (app,s)).start()

def connectClient(app,s):
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=dealData, args=(conn, addr))
        t.start()
        t2 = threading.Thread(target=sendInfo, args=(conn, addr, app))
        t2.start()
 
def sendInfo(conn,addr,app):
    #send the row&col of maze when connected
    conn.send(('size,'+str(app.row)+','+str(app.col)).encode())
    time.sleep(0.01)
    app.connected = True
    while True:
            msg = sendQueue.get()
            conn.send(msg.encode())

def prepareInfo(app):
    if not app.connected: return
    if app.init:
        #reset bomb status
        sendQueue.put('reset')
        app.init = False
    if app.currRow != app.row or app.currCol != app.col:
        #send row&col when updated
        sendQueue.put('size,'+str(app.row)+','+str(app.col))
        app.currRow,app.currCol = app.row,app.col
    #update if p2 can play or not
    if not app.p2Play:
        if app.status in ['Game','Over'] and not app.setting and app.double == 'Enabled':
            sendQueue.put('start')
            app.p2Play = True
    else:
        if app.status not in ['Game','Over'] or app.setting or app.double == 'Disabled':
            sendQueue.put('end')
            app.p2Play = False
    posStr = 'spider,'+str(app.spider.row) + ',' + str(app.spider.col)
    sendQueue.put(posStr)

def dealData(conn, addr):
    print(f"{addr} connected.")
    while True:
        data = conn.recv(1024)
        info = data.decode()
        try:
            posTuple = tuple(info.split(','))
            x,y = int(posTuple[0]), int(posTuple[1])
            recvQueue.put((x,y))
        except:
            pass
    conn.close()

def recvData(app):
    if recvQueue.qsize() > 0:
        x,y = recvQueue.get()
        if not app.setting:
            if app.double == 'Enabled':
                placeBomb(app,0,0,x,y)