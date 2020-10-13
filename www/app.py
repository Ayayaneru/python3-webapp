# -*- coding: utf-8 -*-

__author__ = 'Ayayaneru'

import logging;logging.basicConfig(level=logging.INFO)
import asyncio
from aiohttp import web

async def index(request):
    return web.Response(body=b'<h1>Moe</h1>',content_type='text/html')

def init():
    app=web.Application()
    app.router.add_get('/',index)
    web.run_app(app,host='127.0.0.1',port=9000)

if __name__ == "__main__":
    init()
