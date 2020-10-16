#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Ayayaneru'


# *** day04 begin ***

'''
Models for user, blog, comment.
'''
# 这部分代码抄自蔡老师
# __author__ = 'Michael Liao'
# https://github.com/michaelliao/awesome-python3-webapp/blob/day-04/www/models.py

import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField

def next_id():
    # uuid.uuid4() 可以生成一个随机的 UUID ， 目的是区别不同事务（大概）
    # hex 可以把自身返回为一个16进制整数 ， 所以这个函数就是生成各种 id ，里面还包含时间
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'users'
    # varchar 为 MySQL 里的数据类型
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)
    # time.time 可以设置当前日期和时间， 把日期和时间储存为 float 类型 ， 记录到 create_at 里

class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)

class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)
# 这些属性可以按照自己的需要进行增减


# 之后对数据库的测试在 www 文件夹的 test_sql.py 里