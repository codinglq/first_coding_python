#!/usr/bin/env python
# coding=utf-8

import thread
import server_fun
import socket
import os
#应该添加上字符串太长的问题
msg_len=210

def thread_client(client_sock):
    while True:
        msg_buf_recv=client_sock.recv(msg_len)

        if not msg_buf_recv:
            print '数据接收失败，可能是服务器关闭了，或者网络重名'
            os._exit(0)
        else:
            print '%s:\n内容:%s\n来自:%s' %server_fun.unpack_msg(msg_buf_recv)
#这里应该添加上接受失败的处理

def client_server():
    print '客户端线程'
    #准备握手包
    client_name=raw_input('请输入昵称：')
    str_buf=' hello server'
    msg_buf=server_fun.pack_msg(server_fun.get_time_str(),str_buf,client_name)
    #准备socket通信
    client_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_sock.connect(('127.0.0.1',8080))
    client_sock.send(msg_buf)#发送握手包
    #下面要启动线程用来接收消息
    thread.start_new_thread(thread_client,(client_sock,))
    
    while True:
        send_str_buf=raw_input('请输入要发送的消息:')
        msg_buf=server_fun.pack_msg(server_fun.get_time_str(),send_str_buf,client_name)
        client_sock.send(msg_buf)


#测试客户端
if __name__=='__main__':
    client_server()

