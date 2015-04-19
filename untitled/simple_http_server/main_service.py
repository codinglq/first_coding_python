__author__ = 'lenovo'
#coding=utf-8
import thread
import time
import socket
import os

#将请求中结束去掉请求头，结束CRLF
def clear_head(head_list):
    del head_list[0]
    del head_list[head_list.__len__()-1]
    del head_list[head_list.__len__()-1]
    return head_list

#真正处理求情的线程
def process_callback(remote_fd,remote_addr):
    print '处理来自'+str(remote_addr)+'的请求'
    #准备响应头
    response_head ='HTTP/1.0 200 OK\r\n'
    response_head+='\r\n'
    #remote_fd.send(response_head+'<html><head><title>hello</head><head><body><p>aaa</p></body></html>')
    head_request = ''#浏览器发送来的请求头
    #开始接受浏览器的请求信息，比如请求头啥玩意的。
    #recv函数是阻塞的。
    #可以设置成为非阻塞方式
    #以前的写法是不对的。
    #现在的写法是有问题的，因为缓冲区根本不必那么大
    head_request = remote_fd.recv(1024)
    #print '请求头：',head_request
    kvs_list = head_request.split('\r\n')#请求头的结束是\r\n\r\n请求行的结束是\r\n
    #测试，查看取出来的http头部是否正常
    for e in kvs_list:
        print 'key_value:',e
    #鉴于是个简单的服务器，所以我们只对请求方法和请求资源感兴趣
    #问题来了，不是每次请求都会有完整的请求头？？？？
    resource = ''
    tmp_params_list = kvs_list[0].split(' ')#拆分请求的第一行获取到请求方法和资源
    method = tmp_params_list[0]#请求方法
    resource = tmp_params_list[1]#请求的资源
    print '请求方法：'+method+' 请求资源：'+resource
    #根据http头的规则取出参数,将参数放在字典中，方便后续使用
    params_map = {}#存放参数的字典
    kvs_list = clear_head(kvs_list)
    for e in kvs_list:
        param_dup = e.split(':')
        key = param_dup[0]
        value = param_dup[1]
        params_map[key]=value

    #准备请求的资源
    path = os.path.split(os.path.realpath(__file__))[0]
    resource_path = path + resource.replace('/','\\')
    if resource.endswith('.html'):
        print '开始响应'
        #准备路径
        print path
        print '准备请求的资源:'+resource_path
        res = open(resource_path,'r')
        res_text = res.read().decode('utf-8')
        res.close()
        resp_text = response_head+res_text
        print resp_text
        n = remote_fd.sendall(resp_text)
        remote_fd.close()
    if resource.endswith('.png'):
        print resource_path
        res = open(resource_path,'rb').read()
        print type(res)
        remote_fd.sendall(response_head+res)
        remote_fd.close()
    thread.exit()

#注意，现在只支持静态资源的请求
def main_server(host='127.0.0.1',port=8090,queue_size=10):
    print '服务函数执行'

    server_fd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#socket文件描述符
    server_fd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_fd.bind((host,port))#注意，这里参数是一个元组
    server_fd.listen(queue_size)#最多处理数量
    remote_pool=set()
    while True:
        #开始循环接受请求
        remote_fd,remote_addr = server_fd.accept()
        if remote_addr not in remote_pool:
            remote_pool.add(unicode(remote_addr))
            #注意，启动多线程时候，传输给回调函数的参数应该是元组
            thread.start_new(process_callback,(remote_fd,remote_addr))
        else:
            print '连续请求多次呢？'

if __name__ == '__main__':
    main_server()


