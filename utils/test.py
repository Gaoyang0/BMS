# -*- coding:utf-8 -*-
# Author:DaoYang

import pymysql

def select():

    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "root", "db_bms")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 更新语句
    sql = "SELECT * from app_books"

    try:
        # 执行SQL语句
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            bid = row[0]
            bname = row[1]
            # 打印结果
            print("bid=%s,bname=%s" % (bid, bname))
        print(res)
        # db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    db.close()

if __name__ == '__main__':
    select()