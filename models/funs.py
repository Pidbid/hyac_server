# -*- encoding: utf-8 -*-
"""
@File    :   funs.py
@Time    :   2023/01/08 19:02:25
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   公共函数
"""

# here put the import lib
import json
from bson.json_util import dumps
from models.config import CONFIG

# db = DB()
config = CONFIG()


def rt(code: int, msg: str = None, data: any = None):
    return_context = {"code": code}
    if msg:
        return_context.update({"msg": msg})
    if data:
        return_context.update({"data": data})
    return return_context


def bson2json(data):
    if type(data) == list:
        json_data = []
        for i in data:
            json_data.append(bson2json(i))
        return json_data

    else:
        json_data = json.loads(dumps(data))
        if "children" in data.keys():
            json_data["children"] = bson2json(json_data["children"])
        json_data["_id"] = json_data["_id"]["$oid"]
        return json_data


def db_add_user(username: str, password: str, roles: list):
    user_document = {"username": username, "password": password, "roles": roles}


def init_admin(db):
    """
    init create an admin user account
    create a admin permission user
    """
    pass
