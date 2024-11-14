# -*- encoding: utf-8 -*-
"""
@File    :   user.py
@Time    :   2023/01/08 18:21:08
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
"""

# here put the import lib
import json
from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from models.basemodel import *
from models.db_model import DB_USER

# from models.db import DB
from models.funs import rt, bson2json
from models.passwords import hash_password

from models.token import TOKEN
from models.verifycode import VERIFYCODE

user = APIRouter()
# db = DB()
token = TOKEN()
verifycode = VERIFYCODE()


@user.post("/login")
async def user_login(data: userLogin):
    if await verifycode.verify(data.captcha):
        hashed_pwd = hash_password(data.password)
        res_user = await DB_USER.find_one(
            {"username": data.username, "password": hashed_pwd}
        )
        res_user = res_user.model_dump()
        del res_user["password"]
        if res_user:
            res_token_create = token.create({"username": data.username})
            res_user.update({"token": res_token_create["token"]})
            res_user.update({"tokenExpired": res_token_create["tokenExpired"]})
            return rt(0, "login success", res_user)
        else:
            return rt(1, "username or password was wrong")
    else:
        return rt(1, "verify code was wrong")


@user.post("/captcha")
async def user_code(request: Request):
    code = await verifycode.create(4)
    return rt(200, "success", code)
