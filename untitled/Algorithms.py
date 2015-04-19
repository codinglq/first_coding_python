__author__ = 'lenovo'
#coding=utf-8
#这里封装一些算法，比如权值计算，人员检索结果表的排名算法，等等。
import jieba
import hashlib

class algorithms_family:
    '算法家族，里面尽情的封装算法吧'
    #传入参数是     标签倒排索引，人员信息列表
    #返回计算结果就是计算完成的人员信息表
    def cal_curr_weigth(self,index={'':[]},person_info_list=[]):
        print '计算人员的curr_weight'


    #为了算法的统一性,只有自己使用
    def __cut_chinese__(self,input):
        '中文分词封装'
        return jieba.cut(input)

    #将个人信息中的other进行分词然后放到倒排索引中，给相应编号的人的全局weight加成
    def cut_create_table_index(self,person_info,index,stop_set):
        #通过分词other信息，之后计算全局权值
        other_info = person_info.get_other()
        other_list = jieba.cut(other_info)
        other_list = list(other_list)

        #使用set加快查找速度
        for word  in other_list:
            if word.encode('utf-8') in stop_set:
                print u'移除停用词：' + (word)
                other_list.remove(word)

        #按照other参数计算个人的全局权值
        for other in other_list:
            if index.has_key(other):
                #如果本来索引中就有，那么就把权值加零点五
                person_info.set_global_weight(person_info.get_global_weight() + 0.5)
                print 'person Name:' + person_info.get_name() +' new person Weight:' + unicode(person_info.get_global_weight())
            else:
                #如果原来索引中没有，就添加进去，说明这个是一个新的标签 对于新的标签新的人的权重较大加一
                index[other] = [person_info.get_id()]
                #说明这个是一个新的标签,只需要在倒排索引中添加上这个新标签和对用的人员id即可
                person_info.set_global_weight(person_info.get_global_weight() + 1)
                print 'person Name:'+ person_info.get_name() +  ' new person Weight:' + unicode(person_info.get_global_weight())




##下面测试
if __name__ == '__main__':
    res_list = jieba.cut('我爱你,你是我心中的一首歌')#普通分词模式
    print ','.join(res_list)
    res_list = jieba.cut_for_search('我爱你，你是我心中的一首歌')#搜索引擎分词模式
    print ','.join(res_list).encode('utf-8')

    am = algorithms_family()


    #测试停用词

    #stop = open('D:\\OMG\\find_me\\nlp\\stop_words.txt','r')
    #stop_list = stop.read().split('\n')
    #stop_list = set(stop_list)
    #for e in stop_list:
    #    print  (e)

    #print  type(stop_list)

    #测试md5
    m = hashlib.md5()
    m.update('abcd')
    psw = m.hexdigest()

    print psw

    #print u'你说啥呢？'.encode('gbk')