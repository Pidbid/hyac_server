# -*- encoding: utf-8 -*-
"""
@File    :   collection.py
@Time    :   2023/01/09 23:24:40
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   这里输入一些文件介绍
"""

# here put the import lib
from fastapi import APIRouter, Request

from apps.db.table import sys_db_table
from models.basemodel import *
from models.db import DB
from models.funs import rt

db = DB()
sys_db_collection = APIRouter()
sys_db_collection.include_router(sys_db_table, prefix="/table")


# 数据库集合操作
# 集合获取数据
@sys_db_collection.post("/data")
async def collection_data(data: dataBaseModel):
    collections = db.db_main.list_collection_names()
    return rt(0, None, collections)


# 集合添加
@sys_db_collection.post("/add")
async def collection_add(data: addBaseModel):
    pass


# 集合删除
@sys_db_collection.post("/delete")
async def collection_delete(data: deleteBaseModel):
    pass
