# -*- encoding: utf-8 -*-
"""
@File    :   table.py
@Time    :   2023/01/10 01:10:22
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   这里输入一些文件介绍
"""

# here put the import lib
from fastapi import APIRouter
from models.db import DB
from models.funs import rt
from models.basemodel import *

sys_db_table = APIRouter()


@sys_db_table.post("/data")
async def table_data(data: dataBaseModel):
    pass


@sys_db_table.post("/add")
async def table_add(data: addBaseModel):
    pass


@sys_db_table.post("/delete")
async def table_delete(data: deleteBaseModel):
    pass


@sys_db_table.post("/update")
async def table_update(data: updateBaseModel):
    pass
