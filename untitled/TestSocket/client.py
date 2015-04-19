__author__ = 'lenovo'
#coding=utf-8
#socket 客户端测试
import socket
import time

if __name__ == '__main__':
    print '测试socket 客户端模块'

    addr_ip = socket.gethostbyname('bj.58.com')
    port = 80
    #准备http头信息
    head = open('head.data','rb')
    str_head = head.read()
    #str_head = str_head.replace('\n','\r\n')
    str_head = str_head.replace('#host#','bj.58.com')
    str_head += '\r\n'
    print str_head
    #str_head = 'GET / HTTP/1.1\r\nHost:www.baidu.com\r\nConnection:keep-alive\r\n\r\n'
    head.close()
    socket_dis_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_dis_client.connect((addr_ip,port))

    # 发送请求头
    socket_dis_client.send(str_head)
    #开始接收
    html = ''
    while True:
        recv_msg = socket_dis_client.recv(1048)
        if not len(recv_msg):
            break
        else:
            html+=recv_msg
        #测试客户端关闭break;

    print html
    socket_dis_client.close()



