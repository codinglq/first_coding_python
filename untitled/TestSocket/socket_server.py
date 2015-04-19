__author__ = 'lenovo'
#coding=utf-8
#测试自己还会不会socket了
import socket

if __name__ == '__main__':
    print '测试模块'
    ip_addr = '127.0.0.1'
    port = 8090
    queue_size = 10
    socket_dis = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_dis.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    socket_dis.bind((ip_addr,port))
    socket_dis.listen(queue_size)

    while True:
        connection,remote_addr = socket_dis.accept()
        print 'The Remote Addr is :', remote_addr
        #循环接收数据
        while True:
            print 'start recv......'
            try:
                recv_msg = connection.recv(512)
            except IOError:
                print 'error! remote exception.....'
                connection.close()
                break
            if not recv_msg:
                print 'Ip out line....',remote_addr
                break
            else:
                print 'recv Msg is :'+ recv_msg
                connection.send('hello you!')
        print 'close socket!'
        connection.close()