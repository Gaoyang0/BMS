# -*- coding:utf-8 -*-
# Author:DaoYang


def log(str, type):
    if type == 'book':
        f = open('log/books.log', 'a', encoding='utf-8')
        f.write('\n'+str)
        f.close()
    elif type == 'user':
        f = open('log/users.log', 'a', encoding='utf-8')
        f.write('\n' + str)
        f.close()
    else:
        pass