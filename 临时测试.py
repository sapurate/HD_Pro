# -*- coding:utf-8 -*-
'''
Created on 2019年10月11日

@author: Administrator
'''
#得到列表中某一元素所有位置标号的 列表

def get_index(lst,iem):
    tmp = []
    tag = 0
    for e in lst:
        if e == iem:
            tmp.append(tag)
        tag+=1  #注意自增点别搞错了
    return tmp
# 打印出按序排列的开单量
def Get_Order():
    a = input("请输入开通情况批次集合：")
    b = a.split(",")
    batch_team=[]
    order = []
    c = input("请输入要输出的批次集合：")
    d = c.split(",")
    print(d)
    for i in b:
        if i != '':
            batch_team_order = i.split("@",2)
            batch_team.append(batch_team_order[0]+"@"+batch_team_order[1])
            order.append(batch_team_order[2])
    print(batch_team)

    for j in d:
        if j in batch_team:
            ci_index = get_index(batch_team,j)[0]
            print(order[ci_index])
        else:
            print(0)


if __name__ == '__main__':
    Get_Order()