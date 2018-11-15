#!/usr/bin/env python2
import socket
import sys
from thread import *
import threading

print_lock = threading.Lock()

portToClient={"11111":"H1","11112":"H2","11113":"R1","11114":"R2","11115":"R3","11116":"R4"}
serverPortMapping={"H1":"11121","H2":"11122","R1":"11123","R2":"11124","R3":"11125","R4":"11126"}

def getDV(data):
    lines = data.split(":")
    g = {}
    for i in lines:
        tt=i.split(",")
        g[tt[0]]=tt[1]
    return g

def writeFromG(g,host):
    file = open(host+'.txt', 'w')
    ret=''
    cnt=0
    for key,val in g.iteritems():
        file.write(key+","+val+"\n")
        if(cnt):
            ret=ret+":"+key+","+val
        else:
            ret=ret+key+","+val
        cnt=cnt+1
    return ret

def update(host,data,sPort):
    global mapping
    ff = open(host+'.txt', 'rb')
    f = ff.read().splitlines()
    ff.close()
    x = f[0]
    for i in range(1, (len(f))):
        x = x + ":" + f[i]
    g=getDV(x)
    g1=getDV(data)

    for key,val in g1.iteritems():
        print key+"#"+val
        if(key==host):
            continue
        elif(portToClient[str(sPort)] in g and int(g[key])>int(val)+int(g[portToClient[str(sPort)]])):
            g[key]=str(int(val)+int(g[portToClient[str(sPort)]]))

    return writeFromG(g,host)

def threaded(c,host,sPort):
    while True:
        data = c.recv(1024)
        if not data:
            print_lock.release()
            break
        data = update(host,data,sPort)
        c.send(data)
    c.close()

def Main(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", int(serverPortMapping[host])))
    print("server active at port", serverPortMapping[host])
    s.listen(5)
    print("socket is listening")
    while True:
        c, addr = s.accept()
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(threaded, (c,host,addr[1]))
    s.close()


if __name__ == '__main__':
    if(len(sys.argv)!=2):
        print "Input Error."
    else:
        Main(sys.argv[1])
