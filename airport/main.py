#
#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import time
import sqlite3
import bluetooth
import threading
import minimalmodbus
from minimalmodbus import ModbusException

#服务器套接字(用来接收新链接)
server_socket=None
VFF = '\xFF\x00'
V00 = '\x00\x00'
AutoDelay = 1
ReadOp = 1
WriteOp = 5
#连接套接字服务子线程
def serveSocket(sock,info):
    #开个死循环等待客户端发送信息
    while True:
        #try:
        if True:
            #接收64个字节,然后以UTF-8解码(中文),如果没有可以接收的信息则自动阻塞线程(API)
            cmd = sock.recv(64).decode('utf-8');
            cmdLen = len(cmd)
            msg = 'ok'
            if cmdLen <= 3:
                i = int(cmd[0],10)
                j = int(cmd[1],16)                
                if i>3:
                    return 'unknown inst at %d'%(i)
                if j>15:
                    return 'unknown regester %d'%(j)
                v = 1
                if cmdLen==3:
                    v = int(cmd[2],10)
                msg = handler3(i,j,v)
            elif len(receive)== 2:
                msg = handler2(receive)
            #为了返回好看点,加个换行
            resp=cmd+"_"+msg;
            print('['+str(info)+']'+resp);
            #回传数据给发送者
            sock.send(resp.encode('utf-8'));
        '''except ModbusException as mbExp:
            print('ModbusExp',mbExp)
            sock.send(str(mbExp).encode('utf-8'))
        except Exception as exp:
            print('Exception',exp)
            sock.send(str(exp).encode('utf-8'))'''
#ModBus
 
def handler3(i,j,v):

    if i==0:
        if j==0:
            for k in range(0,16):
                writeReg(inst1,k,V00)
                writeReg(inst2,k,V00)
                time.sleep(0.25)
        elif j==1:
            for k in range(0,16):
                writeReg(inst1,k,VFF)
                writeReg(inst2,k,VFF)
                time.sleep(0.25)
        elif j==3:
            return readAll()
        return 'ok'
    elif i==3:
        return readReg(j)
    
    ctlV = ctlValues[i]
    val = not ctlV[j]
    inst = instList[i]
    writeReg(inst,j,VFF)
    ctlV[j]=val
    return str(val)

def readAll():
    #res1 = inst1.read_registers(0,16)
    res1 = inst1._perform_command(ReadOp,'\x00\x00\x00\x10')
    print('res1',res1)
    res2 = inst2.read_registers(0,16)
    print('res2',bin(res2[0]))
    res2 = ','.join([str(item) for item in res2])
    return res1+res2
    
def setReg(inst,addr):
    addv=bytearray([0,addr])
    inst._perform_command(WriteOp, addv.decode()+VFF)
    tm = threading.Timer(AutoDelay,clearReg,(inst,addr))
    tm.start()
        
def writeReg(inst,addr,val):
    addv=bytearray([0,addr])
    print(addv)
    inst._perform_command(WriteOp, addv.decode()+val)
    #if val==VFF:
    #    tm = threading.Timer(1,clearReg,(inst,addr))
    #    tm.start()

def clearReg(inst,addr):
    addv=bytearray([0,addr])
    inst._perform_command(WriteOp, addv.decode()+V00)
   
def readReg(addr):
    if addr == 0:
        res3 = inst3.read_registers(32,12)
    elif addr < 12:
        res3 = inst3.read_register(32+addr)
    print(res3)
    return str(res3)

#主线程
connect = sqlite3.connect('./bltServer.db')
cursor = connect.cursor()
#创建一个服务器套接字,用来监听端口
server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM);
#允许任何地址的主机连接,未知参数:1(端口号,通道号)
server_socket.bind(("",1))
#监听端口/通道
server_socket.listen(1);

def scanDevice():
    target_name = "My Device"
    target_address = None 
 
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
 
    for bdaddr in nearby_devices:
        if target_name == bluetooth.lookup_name( bdaddr ):
            target_address = bdaddr
            break
 
    if target_address is not None:
        print("found target bluetooth device with address ", target_address)
    else:
        print("could not find target bluetooth device nearby")

inst1 = minimalmodbus.Instrument('/dev/ttySC0', 1,minimalmodbus.MODE_RTU)
inst1.debug=True #inst1.serial.baudrate = 19200
inst2 = minimalmodbus.Instrument('/dev/ttySC0', 2,minimalmodbus.MODE_RTU)
inst2.debug=True

inst3 = minimalmodbus.Instrument('/dev/ttySC0', 3)
instList = [0,inst1,inst2,inst3]
ctlV1 =  [False]*16
ctlV2 =  [False]*16
ctlV3 =  [0.0]*12
ctlValues = [0,ctlV1,ctlV2,ctlV3]

#stage
def raiseStage(ib):
    setReg(inst1,ib)
def clampPlane(ib):
    setReg(inst1,2+ib)
def pushPlane(ib):
    setReg(inst1,4+ib)
def pullPlane(ib):
    setReg(inst1,6+ib)
#bettary
def lockBattery(ib):#servo
    print('lockBattery-',ib)
    
def holdBattery(ib):#
    addv=bytearray([0,8]).decode()
    if ib > 0:
        inst2._perform_command(5, addv+VFF)
    else:
        inst2._perform_command(5, addv+V00)
    
    
def fetchbattery(ib):
    setReg(inst1,8+ib)
def bettary2(ib):
    setReg(inst1,10+ib)
def bettary3(ib):
    setReg(inst1,12+ib)
def bettary4(ib):
    setReg(inst1,14+ib)
    
#cell box
def box1(ib):
    setReg(inst2,0+ib)
def box2(ib):
    setReg(inst2,2+ib)
def box3(ib):
    setReg(inst2,4+ib)
def box4(ib):
    setReg(inst2,6+ib)   
    

 
#开死循环 等待客户端连接
#本处应放在另外的子线程中
while True:
    #等待有人来连接,如果没人来,就阻塞线程等待(这本来要搞个会话池,以方便给不同的设备发送数据)
    sock,info=server_socket.accept();
    #打印有人来了的消息
    print(bluetooth.lookup_name( info[0] ))
    print(str(info[0])+' Connected!');
    #创建一个线程专门服务新来的连接(这本来应该搞个线程池来管理线程的)
    t=threading.Thread(target=serveSocket,args=(sock,info[0]))
    #设置线程守护,防止程序在线程结束前结束
    t.setDaemon(True)
    #启动线程
    t.start();
