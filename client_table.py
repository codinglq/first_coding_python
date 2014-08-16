#!/usr/bin/env python
# coding=utf-8
# coding by iamwall 20140816
#给服务器用的客户端表类里面维护着一个字典
class clinet_table:
    def __init__(self):
        self.client_map={}

    def get_table_size(self):
        return len(self.client_map)

    def is_in_table(self,client_name):
        return self.client_map.has_key(client_name) #判断客户端表中是否有这个名字了
    
    def add_client_member(self,in_name,in_connect):
        #in_name=in_name.strip('\0')#在这里将\0的问题处理掉
        if self.is_in_table(in_name.strip('\0')):
            print '昵称:%s已经存在添加失败'% in_name
            return False
        else:
            self.client_map[in_name.strip('\0')]=in_connect#向客户端表中添加元素
            return True
    
    def del_client_member(self,in_name):
        del self.client_map[in_name.strip('\0')]

    def del_all_client(self):
        del self.client_map

    def get_dict(self):
        return self.client_map
#基本上客户端表就这几个功能吧
