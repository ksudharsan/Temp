#!/usr/bin/env python2
import socket
import sys
import time
from thread import *
import threading

print_lock = threading.Lock()

clientPortMapping={"H1":"11111","H2":"11112","R1":"11113","R2":"11114","R3":"11115","R4":"11116"}
serverPortMapping={"H1":"11121","H2":"11122","R1":"11123","R2":"11124","R3":"11125","R4":"11126"}
neighbor={"H1":["R1"],"R1":["H1","R2","R3"],"R2":["R1","R4"],"R3":["R1","R4"],"R4":["H2","R2","R3"]}
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

def Main(host,host2):
    hostIP='127.0.0.1'
    ff = open(host + '.txt', 'rb')
    f = ff.read().splitlines()
    ff.close()
    x = f[0]
    for i in range(1, (len(f))):
        x = x + ":" + f[i]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", int(clientPortMapping[host])))
    print int(serverPortMapping[host2])
    s.connect((hostIP, int(serverPortMapping[host2])))
    while True:
        s.send(x)
        data = s.recv(1024)
        break
    s.close()


if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print "Input Error."
    else:
        Main(sys.argv[1], sys.argv[2])