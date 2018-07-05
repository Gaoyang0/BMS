# -*- coding:utf-8 -*-
# Author:DaoYang


def query_book(keyword):
    res = {
        'id': '*****',
        'name': '*****',
        'family': '*****'
    }
    limit = keyword.split()
    for item in limit:
        res[get_family(item)] = item
    return res

def get_family(str):
    family = ['哲学', '经济学', '法学', '教育学', '文学', '历史学', '理学', '工学', '农学', '医学', '军事学', '管理学', '其他']
    if str.isdigit():
        return 'id'
    elif str in family:
        return 'family'
    else:
        return 'name'


if __name__ == "__main__":
    query_book('哲学')