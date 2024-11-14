# -*- encoding: utf-8 -*-
"""
@File    :   router.py
@Time    :   2024/11/14 15:41:24
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
"""

# here put the import lib
from bson import ObjectId
from datetime import datetime
from fastapi import APIRouter, Request

from models.basemodel import *
from models.funs import rt, bson2json
from models.db_model import DB_ROUTER, DB_APPLICATION
from models.passwords import generate_rand_str

sys_router = APIRouter()


@sys_router.post("/data")
async def router_data(request: Request, data: dataBaseModel):
    pass


@sys_router.post("/create")
async def router_create(request: Request, data: routerCreateModel):
    # check application exist
    app_res = await DB_APPLICATION.find_one(DB_APPLICATION.appid == data.appid)
    if not app_res:
        return rt(0, "wrong")
    if request.state.tokeninfo["username"] not in app_res.model_dump()["belongs"]:
        return rt(0, "wrong")
    if data.parent_id:
        # create child path
        router_res = await DB_ROUTER.find_one(
            DB_ROUTER.path == data.path, DB_ROUTER.parent_id == data.parent_id
        )
        if not router_res:
            add_router_res = await DB_ROUTER(
                path=data.path, parent_id=data.parent_id, mode=data.mode
            ).insert()
            router_res = await DB_ROUTER.find_one(
                DB_ROUTER.path == data.path, DB_ROUTER.parent_id == data.parent_id
            )
            return rt(0, "create router success", router_res)
        else:
            return rt(1, "same path and parent_id")
    else:
        # create route path
        router_res = await DB_ROUTER.find_one(DB_ROUTER.path == data.path)
        if router_res:
            return rt(1, "same path and parent_id")
        else:
            add_router_res = await DB_ROUTER(
                appid=data.appid, path=data.path, mode=data.mode
            ).insert()
            router_res = await DB_ROUTER.find_one(
                DB_ROUTER.path == data.path, DB_ROUTER.parent_id == data.parent_id
            )
            return rt(0, "create router success", router_res)


@sys_router.post("/delete")
async def router_delete(request: Request, data: routerDeleteModel):
    router_res = await DB_ROUTER.get(data.id)
    if not router_res:
        return rt(1, "router not exist")
    appid = router_res.model_dump()["appid"]
    app_res = await DB_APPLICATION.find_one(
        DB_APPLICATION.appid == appid,
        DB_APPLICATION.belongs == request.state.tokeninfo["username"],
    )
    if not app_res:
        return rt(1, "you don not have permission")
    # delete operate
    delete_res = await router_res.delete()
    if delete_res.deleted_count:
        return rt(0, "delete route success")
    else:
        return rt(1, "wrong")


@sys_router.post("/update")
async def router_update(request: Request, data: dataBaseModel):
    pass
