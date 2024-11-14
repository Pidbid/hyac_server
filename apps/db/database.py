# -*- encoding: utf-8 -*-
"""
@File    :   database.py
@Time    :   2023/01/09 23:24:30
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   这里输入一些文件介绍
"""

# here put the import lib
from fastapi import APIRouter, Request

from apps.db.collection import sys_db_collection
from models.basemodel import *
from models.db import DB
from models.funs import rt

db = DB()
sys_database = APIRouter()
sys_database.include_router(sys_db_collection, prefix="/collection")


# 数据库表操作
# 获取数据库列表
@sys_database.get("/data")
async def database_data():
    collections = db.client_main.list_database_names()
    return rt(0, "success", collections)


# 创建新的数据库
@sys_database.post("/add")
async def database_add(data: addBaseModel):
    pass


# 数据库删除
@sys_database.post("/delete")
async def database_delete(data: deleteBaseModel):
    res_delete = db.client_main.drop_database(data.name)
    return rt(0, None, res_delete)
