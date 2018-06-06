# -*- coding: UTF-8 -*-
import io
import sys
import pymysql as pymysql
import collections


class MyDict(dict):  # 有序字典实现

    def __init__(self):
        self.li = []
        super(MyDict, self).__init__()

    def __setitem__(self, key, value):
        self.li.append(key)
        super(MyDict, self).__setitem__(key, value)

    def __str__(self):
        temp_list = []
        for key in self.li:
            value = self.get(key)
            temp_list.append("'%s':'%s'" % (key, value,))
        temp_str = '{' + ','.join(temp_list) + '}'
        return temp_str

db = pymysql.connect("localhost", "root", "root", "zhihu", charset='utf8')
cursor = db.cursor()
a = None
try:
    for var in '新':
        sql = "SELECT url FROM get_url WHERE word = '" + var + "'"
        cursor.execute(sql)
        results = cursor.fetchall()
        if a is None:
            a = set(results)
        else:
            a = a & set(results)
except:
    print("Error: unable to fetch data")
re = {}
for var in a:
    sql = "select title,score from get_title where url ='" + var[0]+"'";
    cursor.execute(sql)
    data = cursor.fetchone()
    re[var[0]] = data
print(re)
sortRe = MyDict()
for var in sorted(re.items(), key=lambda e:e[1][1], reverse=True):
    sortRe[var[0]] = var[1][0]
print(sortRe)
db.close()