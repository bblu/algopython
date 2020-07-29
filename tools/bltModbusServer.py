#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import time
import bluetooth
import threading
import minimalmodbus
from minimalmodbus import ModbusException
#服务器套接字(用来接收新链接)
server_socket=None
VFF = '\xFF\x00'
V00 = '\x00\x00'
#连接套接字服务子线程
def serveSocket(sock,info):
    #开个死循环等待客户端发送信息
    while True:
        #try:
        if True:
            #接收64个字节,然后以UTF-8解码(中文),如果没有可以接收的信息则自动阻塞线程(API)
            receive=sock.recv(64).decode('utf-8');
            #打印刚刚读到的东西(info=地址)
            msg = 'ok'
            if(len(receive)==1):
                msg = handler1(receive)
            elif len(receive)== 2:
                msg = handler2(receive)
            #为了返回好看点,加个换行
            receive=receive+"_"+msg;
            print('['+str(info)+']'+receive);
            #回传数据给发送者
            sock.send(receive.encode('utf-8'));
        '''except ModbusException as mbExp:
            print('ModbusExp',mbExp)
            sock.send(str(mbExp).encode('utf-8'))
        except Exception as exp:
            print('Exception',exp)
            sock.send(str(exp).encode('utf-8'))'''
#ModBus
 
def handler2(cmd):
    i = int(cmd[0],10)
    j = int(cmd[1],16)
    if i==0:
        if j==1:
            k=0
            while True:
                writeReg(inst1,k%16,VFF)
                k = k+1
                time.sleep(0.25)
        if j==3:
            return readAll()
            
    if i>3:
        return 'unknown inst at %d'%(i)
    if j>15:
        return 'unknown regester %d'%(j)
    ctlV = ctlValues[i]
    val = not ctlV[j]
    inst = instList[i]
    writeReg(inst,j,VFF)
    ctlV[j]=val
    return str(val)

def readAll():
    res = inst1.read_registers(0,16)
    print(res)
    return ','.join([str(item) for item in res])
    
def writeReg(inst,addr,val):
    addv=bytearray([0,addr])
    print(addv)
    inst._perform_command(5, addv.decode()+val)
    if val==VFF:
        tm = threading.Timer(1,clearReg,(inst,addr))
        tm.start()

def clearReg(inst,addr):
    addv=bytearray([0,addr])
    inst._perform_command(5, addv.decode()+V00)

#主线程
 
#创建一个服务器套接字,用来监听端口
server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM);
#允许任何地址的主机连接,未知参数:1(端口号,通道号)
server_socket.bind(("",1))
#监听端口/通道
server_socket.listen(1);

inst1 = minimalmodbus.Instrument('/dev/ttySC0', 1,minimalmodbus.MODE_RTU)
inst1.debug=True #inst1.serial.baudrate = 19200

inst2 = minimalmodbus.Instrument('/dev/ttySC0', 2)
inst3 = minimalmodbus.Instrument('/dev/ttySC0', 3)
instList = [0,inst1,inst2,inst3]
ctlV1 =  [False]*16
ctlV2 =  [False]*16
ctlV3 =  [0.0]*12
ctlValues = [0,ctlV1,ctlV2,ctlV3]
 
#开死循环 等待客户端连接
#本处应放在另外的子线程中
while True:
    #等待有人来连接,如果没人来,就阻塞线程等待(这本来要搞个会话池,以方便给不同的设备发送数据)
    sock,info=server_socket.accept();
    #打印有人来了的消息
    print(str(info[0])+' Connected!');
    #创建一个线程专门服务新来的连接(这本来应该搞个线程池来管理线程的)
    t=threading.Thread(target=serveSocket,args=(sock,info[0]))
    #设置线程守护,防止程序在线程结束前结束
    t.setDaemon(True)
    #启动线程
    t.start();
