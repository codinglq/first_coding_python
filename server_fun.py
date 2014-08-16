#!/usr/bin/env python
# coding=utf-8
#服务器用到的函数
#单元测试不要忘
#coding by iamwall 20140816 python 网络聊天室
# fuck的  一个字符串的问题搞了一下午 原来python中的字符串结束不是\0
import client_table
import struct
import socket
import thread
import time

msg_len=210
ip_address='127.0.0.1'
port=8080
format='100s100s10s'

def get_time_str():
    local_time=time.localtime(time.time())
    local_time=time.asctime(local_time)
    return local_time.__str__()

def pack_msg(local_time,in_str,in_name):#将要发送的数据打包
    temp_pack=struct.pack(format,local_time,in_str,in_name)
    return temp_pack


def unpack_msg(in_msg_pack):#将数据解包 格式为连天内容 昵称
    return struct.unpack(format,in_msg_pack)


def send_msg_to_all(in_msg,in_client_table):#给表中的连接发送数据
#我靠 没有类型 解释器在运行时候也不知道是什么类型的  我靠
    print '客户端表中链接个数:%d' %in_client_table.get_table_size()
    for (client_name,client_sock) in in_client_table.get_dict().items():
        if not (client_name==unpack_msg(in_msg)[2].strip('\0')):
            #如果是自己的连接 则不发送
            try:
                client_sock.send(in_msg)
            except BaseException:
                print '服务器发送失败'
        else:
            print '不用给发送这个消息的客户端发送消息了'


def thread_opt(client_connection,client_name,server_table):
    #处理客户端链接的线程回调函数
    while True:
        msg_buf=client_connection.recv(msg_len)
        if not msg_buf:
            print '客户端:%s下线了' %client_name
            #还要在客户端表中删除这个项
            server_table.del_client_member(client_name)
            thread.exit()
        else:
            send_msg_to_all(msg_buf,server_table)#这里就这么短啊



def start_server():
    server_table=client_table.clinet_table()
    #定义服务器上的客户端表
    #下面准备tcp通信
    server_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#获取描述符
    server_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#设置端口重用
    server_sock.bind(('127.0.0.1',8080))#这个地方的ip应该整成可变的
    server_sock.listen(50)
    #主线程维护客户端表 子线程搞定客户端
    while True:
        print '等待客户端接入：'
        client_connection,client_address=server_sock.accept()
        #在这里接收握手包
        first_msg=client_connection.recv(msg_len)
        #装载到客户端表中

        if server_table.add_client_member(unpack_msg(first_msg)[2],client_connection):
            #这里是将客户端链接成功添加到了客户端表中了  下面该启动线程了
            print '为:%s启动线程' %unpack_msg(first_msg)[2]
            print client_address
            #开始启动线程
            thread.start_new_thread(thread_opt,(client_connection,unpack_msg(first_msg)[2],server_table))
        else:
            print '重名了'
            error_name_msg=pack_msg(get_time_str(),'网络重名','服务器消息')
            client_connection.send(error_name_msg)
            client_connection.close()

#测试模块
if __name__=='__main__':
    start_server()

