# -*- encoding: utf-8 -*-
"""
@File    :   application.py
@Time    :   2023/01/10 20:25:49
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   application action api
"""

# here put the import lib
from datetime import datetime
from fastapi import APIRouter, Request

from models.basemodel import *
from models.funs import rt, bson2json
from models.db_model import DB_APPLICATION
from models.passwords import generate_rand_str

sys_apps = APIRouter()


@sys_apps.post("/data")
async def apps_data(request: Request, data: dataBaseModel):
    res_apps = (
        await DB_APPLICATION.find_many(
            DB_APPLICATION.belongs == request.state.tokeninfo["username"]
        )
        .skip((data.page - 1) * data.length)
        .limit(data.length)
        .to_list()
    )
    if res_apps:
        return rt(0, "success", {"data": res_apps, "count": data.length})
    else:
        return rt(0, "empty", {"data": [], "count": 0})


@sys_apps.post("/create")
async def apps_create(request: Request, data: applicationCreateModel):
    app_res = await DB_APPLICATION.find_one(DB_APPLICATION.name == data.name)
    if not app_res:
        app_str8 = generate_rand_str(8)
        # make sure appid is unique
        while True:
            app_res = await DB_APPLICATION.find_one(DB_APPLICATION.appid == app_str8)
            if app_res:
                app_str8 = generate_rand_str(8)
            else:
                break
        app_str16 = generate_rand_str(16)
        add_app = DB_APPLICATION(
            name=data.name,
            appid=app_str8,
            createTime=datetime.now(),
            updateTime=datetime.now(),
            dbName=app_str8,
            dbUser=app_str8,
            dbPwd=app_str16,
            imports=[],
            tokenSalt=app_str16,
            status="creating",
            belongs=[request.state.tokeninfo["username"]],
            cpu=data.cpu,
            memory=data.memory,
        )
        add_app_res = await add_app.insert()
        # fastapi background task

        app_res = await DB_APPLICATION.find_one(DB_APPLICATION.appid == app_str8)
        return rt(0, "create app success", app_res.model_dump(exclude=["id"]))
    else:
        return rt(1, "same name app exist,please change app name")


@sys_apps.post("/delete")
async def apps_delete(request: Request, data: applicationDeleteModel):
    app_res = await DB_APPLICATION.find_one(
        DB_APPLICATION.appid == data.appid,
        DB_APPLICATION.belongs == request.state.tokeninfo["username"],
    ).delete()
    if app_res.deleted_count == 1:
        return rt(0, "delete app success", {"appid": data.appid})
    else:
        return rt(1, "delete failed")


# get single application info
@sys_apps.post("/info")
async def apps_info(request: Request, data: applicationInfo):
    res_info = await DB_APPLICATION.find_one(
        DB_APPLICATION.appid == data.appid,
        DB_APPLICATION.belongs == request.state.tokeninfo["username"],
    )
    if res_info:
        return {"code": 0, "msg": "success", "data": res_info}
    else:
        return {"code": 1, "msg": "appid wrong"}


# update application settings
@sys_apps.post("/update")
async def apps_update(request: Request, data: applicationUpdateModel):
    update_data = {}
    if data.cpu:
        update_data["cpu"] = data.cpu
    if data.memory:
        update_data["memory"] = data.memory
    update_res = await DB_APPLICATION.find_one(
        DB_APPLICATION.appid == data.appid,
        DB_APPLICATION.belongs == request.state.tokeninfo["username"],
    ).update_one({"$set": update_data})
    if update_res.matched_count > 0:
        return rt(0, "update success", {"appid": data.appid})
    else:
        return rt(1, "update failed")
