#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Ayayaneru'
# 蔡老师的源码跑出了两个错误，这里暂时用的凹酱,源码见下
# https://github.com/yzyly1992/2019_Python_Web_Dev/blob/master/www/orm.py


# *** day03 begin ***

import asyncio, logging, aiomysql

# 创建基本日志函数，变量 sql 出现了很多次，这里我们还不知道它的作用
def log(sql, args=()):
    logging.info('SQL: %s' % sql)

# 异步IO起手式 async ，创建连接池函数， pool 用法见下：
# https://aiomysql.readthedocs.io/en/latest/pool.html?highlight=create_pool
async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    # 声明 __pool 为全局变量
    global __pool
    # 使用这些基本参数来创建连接池
    # await 和 async 是联动的（异步IO）
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )

async def select(sql, args, size=None):
    log(sql, args)
    global __pool
    # with-as: 可以方便我们执行一些清理工作，如 close 和 exit：
    # https://www.jianshu.com/p/c00df845323c

    # 这里的 await 很多，可能看不懂什么意思，我暂时把它理解为：
    # 可以让它后面执行的语句等一会，防止多个程序同时执行，达到异步效果
    with (await __pool) as conn:
        # cursor 叫游标，conn没懂，应该也是个‘池’
        # 'aiomysql.DictCursor'看似复杂，但它仅仅是要求返回字典格式
        cur = await conn.cursor(aiomysql.DictCursor)
        # cursor 游标实例可以调用 execute 来执行一条单独的 SQL 语句，参考自：
        # https://docs.python.org/zh-cn/3.8/library/sqlite3.html?highlight=execute#cursor-objects
        # 这里的 cur 来自上面的 conn.cursor ，然后执行后面的 sql ，具体sql干了啥先不管
        await cur.execute(sql.replace('?', '%s'), args or())
        # size=None 时为 False，上面定义了初始值为 None ，具体得看传入的参数有没有定义 size
        if size:
            # fetchmany 可以获取行数为 size 的多行查询结果集，返回一个列表
            rs = await cur.fetchmany(size)
        else:
            # fetchall 可以获取一个查询结果的所有（剩余）行，返回一个列表
            rs = await cur.fetchall()
        #  close() ，立即关闭 cursor ，从这一时刻起该 cursor 将不再可用
        await cur.close()
        # 日志：提示返回了多少行
        logging.info('rows returned: %s' % len(rs))
        # 现在我们知道了，这个 select 函数给我们从 SQL 返回了一个列表
        return rs

async def execute(sql, args):
    log(sql)
    with (await __pool) as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'),args)
            # rowcount 获取行数，应该表示的是该函数影响的行数
            affected = cur.rowcount
            await cur.close()
        except BaseException as e:
            # 将错误抛出，BaseEXception 是异常不用管
            raise
        # 返回行数
        return affected

# 今天先摸了，写这么多注释也是一个学习的过程 2020/10/14



