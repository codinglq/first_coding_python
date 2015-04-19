__author__ = 'lenovo'
#coding:utf-8

import json
from PersonInfo import person_info
from Algorithms import algorithms_family
#小测试索引类，暂时不用
class index_inner:
    '倒排索引类'
    name = r's'
    def __init__(self):
        #索引类的内部实现是一个字典类型
        self.index={r'':[[]]}

    #获取到内部索引
    def get_index(self):
        return self.index

    #添加一个索引条目，标签列表-信息列表 其中信息列表为 [姓名，权值，部门]
    def set_person_info(self,tag_str_list,list_info):
        list_len = len(tag_str_list)-1
        print(r'开始插入')
        print(r'len:'+str(list_len))
        while 0<=list_len:
            #调试输出
            if self.index.has_key(tag_str_list[list_len]):
                self.index[tag_str_list[list_len]].append(list_info)#向对应的tag里面添加人员信息,如果原来没有存在的tag，那么就自动添加上了。
            else:
                self.index[tag_str_list[list_len]] = []
                #向列表中，添加列表
                self.index[tag_str_list[list_len]].append(list_info)

            list_len = list_len-1

    #从索引中获取信息，通过标签
    def get_person_info(self,tag_str_list):
        #获取到的应该是一个列表，列表中是按照权值排序的人名，部门等 今后需要扩展
        list_len  = len(tag_str_list)-1
        res_list = []#注意，这里是列表中包含列表
        while 0<=list_len:
            if self.index.has_key(tag_str_list[list_len]):
                temp_res = self.index[tag_str_list[list_len]]
                res_list = res_list+(temp_res)
            list_len = list_len-1

        #排序  省略
        #去重
        return res_list



#这个应该写成一个单例
class person_table:
    '人员信息表，中间存储着所有的人员信息的列表以及具备查找的功能'

    #采用单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            orig = super(person_table,cls)
            cls._instance = orig.__new__(cls,*args,**kw)
        return cls._instance

    #设定一些参数
    def __init__(self):
        self.__person_list = []
        self.__curr_max_id = 0
        self.__index = {'':[]}#倒排索引
        self.__index_research = {'':[]}#反向索引，通过人名查找人，一键多值模型,应该在load时候就生成
    #将文件中的人员信息转化成自己定义的对象
    def __conver__(self,person_info_list):
        for e in person_info_list:
            psn = person_info(e['name'],e['department'],e['other'],self.__curr_max_id,e['tag'].split(','))
            self.__curr_max_id = self.__curr_max_id+1
            self.__person_list.append(psn)

    #从文件读取信息，建立人员信息表
    def load_person_info(self,file_path):
        #由于这里有文件读写，所以可能会出现异常
        try:
            file_json = open(file_path,'r')
            str_json  = file_json.read()
        except IOError:
            print 'json文件读取失败'
        else:
            print 'josn知识库加载成功'
            file_json.close()#千万不要忘记关闭文件
        #有时候可能会因为带有换行符出现bug，所以暂时保留
        #str_json = str_json.replace('\\n','')
        #str_json = str_json.replace('\r\n','')
        #从文件读取json格式的人员信息
        obj = json.loads(str_json)
        self.__conver__(obj)
        #建立反向查找表  加载的时候顺便建立反向查找表
        for person in self.__person_list:
            psn_id = person.get_id()
            psn_name = person.get_name()
            if self.__index_research.has_key(psn_name):
                self.__index_research[psn_name].append(psn_id)
            else:
                self.__index_research[psn_name] = [psn_id]

        return self.__person_list

    #获取个人信息表
    def get_person_table(self):
        return self.__person_list
    #根据ID获取个人信息
    def get_person_info_by_id(self,id):
        return self.__person_list[id]

    #生成倒排索引算法开始啦
    #下次添加上权值计算
    def make_index(self):
        #遍历人员信息表，然后遍历每个人的标签，生成倒排索引
        for person in self.__person_list:
            #如果索引中有这个标签，就向索引中添加这个人的ID，否则就添加这个标签和ID
            for tag in person.get_tag():
                #print  unicode(tag)
                if self.__index.has_key(tag):
                    self.__index[tag].append(person.get_id())
                else:
                    self.__index[tag] = [person.get_id()]
        #生成完成倒排索引，顺便就将个人的全局权值计算一下。
        am = algorithms_family()
        #出去停用词
        try:
            stop_words = open('D:\\OMG\\find_me\\nlp\\stop_words.txt','r')
        except IOError:
            print '停用词文件加载失败！'
        else:
            print '停用词文件加载成功！'

        stop_list = stop_words.read()
        stop_list = stop_list.split('\n')
        stop_set = set(stop_list)#将停用词转换成set集合，之后加快查找速度
        #使用完之后不要忘记关闭文件
        stop_words.close()

        print '计算个人信息中的全局权值'
        for psn in self.__person_list:
            am.cut_create_table_index(psn,self.__index,stop_set)

    #根据输入的标签，检索相关人员
    def search_person(self,input_tag_list=[]):
        res_list = []
        for tag in  input_tag_list:
            tag = tag.decode('utf-8')
            if self.__index.has_key(tag):
                res_list = res_list + self.__index[tag]
            ##需要在这里去重和进行排名
        return res_list

    #根据人名，反向查找人员信息
    def research_person(self,name_list):
        temp_list = []
        for name in name_list:
            name = name.decode('utf-8')
            if self.__index_research.has_key(name):
                temp_list = temp_list + self.__index_research[name]

        return temp_list


#测试模块
if __name__ == '__main__':
    p = lambda person: unicode(person)
    print('测试模块person')
    test_load = person_table()
    test_load.load_person_info('D:\\OMG\\find_me\\input.json')
    #开始建立索引
    test_load.make_index()
    #for e in test_load.get_person_table():
    #    print unicode(e)

    #检索测试
    print '开始检索'

    #测试反向查找
    name_list = ['liqiang','gaoxiaosong','lilianjie']

    res = test_load.research_person(name_list)
    print type(res)
    for e in res:
        print unicode(test_load.get_person_info_by_id(e))
