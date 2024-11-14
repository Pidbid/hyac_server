# -*- encoding: utf-8 -*-
"""
@File    :   config.py
@Time    :   2023/01/13 15:19:51
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   config init route
"""

# here put the import lib
from fastapi import APIRouter

from modules.basemodel import *
from modules.db import DB
from modules.funs import bson2json, rt

db = DB()


sys_config = APIRouter()


@sys_config.post("/info")
async def init_info(data: initConfig):
    res_info = db.dbt_config.find_one({"mode": data.mode})
    return rt(0, "success", bson2json(res_info)["data"])
