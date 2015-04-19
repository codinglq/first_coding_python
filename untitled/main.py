__author__ = r'lenovo'
#coding:utf-8
import Index
#mian 函数  test使用
# index = Index.index_inner()
#
# for e in res_list:
#     for a in e:
#         print a
#     print '\n'
#
# #####
# b = Index.index_inner()
# a = [b]
#print type(a)


#测试人员类
ps1  = Index.person_info('liqiang','','this is Other',2,9)
ps2 = Index.person_info('zhang1','页')
lis = [ps1,ps2]
for e in lis:
    print e
