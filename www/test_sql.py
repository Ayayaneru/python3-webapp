#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Ayayaneru'
# 接着 models.py 继续， 对数据库进行测试， 数据库的知识参考蔡老师的教程：
# https://www.liaoxuefeng.com/wiki/1177760294764384


# 这里对我们前面写的进行测试， 看看能不能工作
# 安装好 MySQL 后， 第一步：从开始菜单打开 'MySQL Notifier 1.1.8' ，并在任务栏中开启它
# 第二步：开始菜单打开 'MySQL 5.6 Command Line Client' ，并输入安装时你设置的 root 密码
# 输密码的时候不会显示密码，你只管输，然后回车
# 第三步：把下面注释的代码复制到 SQL 命令行里，然后回车
# 这里初始化了一个名为 moe 的数据库表
'''
-- schema.sql

drop database if exists moe;
drop user if exists 'www-data'@'localhost';

create database moe;

use moe;

create user 'www-data'@'localhost' identified by 'www-data';
alter user 'www-data'@'localhost' identified with mysql_native_password by 'www-data';
grant select, insert, update, delete on moe.* to 'www-data'@'localhost';

create table users (
    `id` varchar(50) not null,
    `email` varchar(50) not null,
    `passwd` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_at` real not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table blogs (
    `id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `name` varchar(50) not null,
    `summary` varchar(200) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table comments (
    `id` varchar(50) not null,
    `blog_id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;
'''

# 第四步：把下面这部分代码放在 python 里跑 （直接跑我这个 test_sql.py 也行）
import orm
import asyncio
from models import User, Blog, Comment
# 这部分源码来自 https://aodabo.tech/blog/001546713871394a2814d2c180b4e6f8d30c62a3eaf218a000
async def test(loop):                      # *** 注意此处的密码填自己设的密码 ***
    await orm.create_pool(loop=loop, user='root', password='369874125', db='moe')
                                           # *** 注意此处的密码填自己设的密码 ***
    u = User(name='Test', email='test@qq.com', passwd='1234567890', image='about:blank')
    await u.save()
    ## 网友指出添加到数据库后需要关闭连接池，否则会报错 RuntimeError: Event loop is closed
    orm.__pool.close()
    await orm.__pool.wait_closed()
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    loop.close()

# 第五步：在 sql 命令行里输入 'SELECT * FROM users;'  然后回车（别漏了分号）
# 显示 test@qq.com 代表测试成功了