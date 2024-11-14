# -*- encoding: utf-8 -*-
"""
@File    :   function.py
@Time    :   2023/01/13 17:53:24
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   route function about functions
"""

# here put the import lib
import time
from fastapi import APIRouter, Request

from models.basemodel import *
from models.db import DB
from models.funs import rt, bson2json
from models.passwords import generate_rand_str
from models.db_model import DB_FUNCTION, DB_APPLICATION

db = DB()
sys_function = APIRouter()


@sys_function.post("/info")
async def function_info(data: functionInfo):
    info_func = db.dbt_apps_function.find_one(
        {"appid": data.appid, "id": data.functionid}
    )
    return rt(0, "get function info success", bson2json(info_func))


@sys_function.post("/create")
async def function_create(request: Request, data: functionCreateModel):
    app_res = await DB_APPLICATION.find_one(
        DB_APPLICATION.appid == data.appid,
        DB_APPLICATION.belongs == request.state.tokeninfo["username"],
    )
    if not app_res:
        return rt(1, "you dot't have permission")
    func_id = generate_rand_str(16)
    while True:
        func_res = await DB_FUNCTION.find_one(DB_FUNCTION.funcid == func_id)
        if func_res:
            func_id = generate_rand_str(16)
        else:
            break
    current_time = datetime.now()
    add_res = await DB_FUNCTION(
        appid=data.appid,
        funcid=func_id,
        mode=data.mode,
        description=data.description,
        tag=data.tag,
        code=data.code,
        router="",
        createTime=current_time,
        updateTime=current_time,
    ).insert()
    return rt(0, "create function success")


@sys_function.post("/update")
async def function_update(data: functionUpdate):
    res_update = db.dbt_apps_function.update_one(
        {"id": data.functionid}, {"$set": data.data}
    )
    print(res_update)
    return rt(0, "function update success")


@sys_function.post("/delete")
async def function_delete():
    """
    删除函数
    """
    pass


@sys_function.post("/tags")
async def function_tags(data: applicationInfo):
    res_tag = db.dbt_apps_function.find({"appid": data.appid})
    tags = []
    for t in res_tag:
        tags = list(set(tags + t["tag"]))
    return rt(0, "get function tags success", tags)
