# -*- encoding: utf-8 -*-
"""
@File    :   main.py
@Time    :   2023/01/07 18:52:35
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
"""

# here put the import lib
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from models.config import CONFIG
from apps.sys import sys_services
from models.db import DB
from models.middleware import MwJwttoken
from models.etcd import ETCD

# 初始化配置
db = DB()
config = CONFIG()
etcd = ETCD()
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# add middleware
app.add_middleware(middleware_class=MwJwttoken)


@app.on_event("startup")
async def db_init():
    await db.db_init()
    await db.__init_admin_account__()
    await db.__init_settings__()
    etcd.__db_init__()  # put database password to etcd


# 系统操作
app.include_router(sys_services, prefix="/sys")


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=5555)
