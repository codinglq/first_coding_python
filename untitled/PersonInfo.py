__author__ = 'lenovo'
#coding=utf-8
class person_info:
    '人员信息类'
    def __init__(self,the_name='null',the_department='null',the_other='null',the_id=0,the_tag=[],the_curr_weight=0,the_global_weight=0.0):
        self.__id = the_id#全局id
        self.__name = the_name#姓名，不一定是唯一的
        self.__department = the_department#部门
        self.__other = the_other#其他信息，比如部门中负责的模块，这个也要作为检索排名的依据
        self.__curr_weight = the_curr_weight#当前部门权重
        self.__global_weight = the_global_weight#全局的权重
        self.__tag = the_tag#标签列表
        #将来是否可以加上联系电话啥的
    def __str__(self):
        tag = ''
        for e in self.__tag:
            tag = tag + e + ' '
        return 'PersonInfo:' + self.__name + ' DepartMent:' + self.__department + ' OtherInfo:' + self.__other + ' CurrWeight:' + str(self.__curr_weight) + ' GlobalWeight:'+ str(self.__global_weight)+' Id:' + str(self.__id) + '\n'+ ' Tag:' +tag
#getter
    def get_name(self):
        return self.__name

    def get_department(self):
        return self.__department

    def get_other(self):
        return self.__other

    def get_curr_weight(self):
        return self.__curr_weight

    def get_id(self):
        return self.__id

    def get_global_weight(self):
        return self.__global_weight
    def get_tag(self):
        return self.__tag
#end getter

#setter
    def set_name(self,the_name):
        self.__name = the_name

    def set_department(self,the_department):
        self.__department = the_department

    def set_other(self,the_other):
        self.__other = the_other

    def set_curr_weight(self,the_curr_weight):
        self.__curr_weight = the_curr_weight

    def set_id(self,the_id):
        self.__id = the_id

    def set_global_weight(self,the_global_weight):
        self.__global_weight = the_global_weight
#end setter