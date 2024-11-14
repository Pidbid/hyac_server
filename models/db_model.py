# -*- encoding: utf-8 -*-
"""
@File    :   db_modal.py
@Time    :   2023/08/25 23:39:39
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   这里输入一些文件介绍
"""

# here put the import lib
import pymongo
from typing import List, Union, Optional, Any
from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from models.basemodel import userProfileModel, dbApplicationStatus, dbRoutersMode


# 用户身份
db_user_roles = ["admin", "user"]
# 用户按钮权限
db_user_btn_roles = ["btn.add", "btn.del", "btn.edit", "btn.link"]
# 用户登录场景
db_verifycode_scene = ["login", "register"]
# application different status
# db_application_status = ["creating","starting","running","stopping","stopped","deleting","deleted"]


class DB_USER_LOGIN(Document):
    username: str
    password: str


# 默认用户模型
class DB_USER(Document):
    username: str = None
    password: str = None
    createTime: datetime = None
    updateTime: datetime = None
    roles: Union[List[str], None] = Union[
        Field(type=list, items=str, choices=db_user_roles), None
    ]
    profile: userProfileModel

    def dict(self, *args, **kwargs):
        return super().dict(*args, **kwargs, exclude={"revision_id"})

    class Settings:
        name = "sys-users"


# 无密码的用户模型
class DB_USER_NPW(Document):
    username: str
    createTime: datetime = None
    updateTime: datetime = None
    roles: List[str] = Field(type=list, items=str, choices=db_user_roles)
    authBtnList: List[str] = Field(type=list, items=str, choices=db_user_btn_roles)

    class Settings:
        name = "sys-users"


class DB_VERIFYCODE(Document):
    code: str
    expired: datetime
    scene: str = Field(type=str, choices=db_verifycode_scene)

    class Settings:
        name = "sys-verifycode"
        indexes = [
            pymongo.IndexModel(
                [("expired", pymongo.ASCENDING)],
                expireAfterSeconds=10,  # 这里设置为3600秒后过期，即1小时
            ),
        ]


# 应用数据库
class DB_APPLICATION(Document):
    appid: str
    name: str
    createTime: datetime
    updateTime: datetime
    dbName: str
    dbUser: str
    dbPwd: str
    imports: List[str]
    tokenSalt: str
    status: dbApplicationStatus
    belongs: List[str]
    cpu: str
    memory: str

    class Settings:
        name = "sys-apps"


# settings database model
class DB_SETTING(Document):
    mode: str
    description: Optional[str] = ""
    data: Any

    class Settings:
        name = "sys-settings"


# router
class DB_ROUTER(Document):
    appid: str
    path: str
    parent_id: Optional[str] = ""
    mode: dbRoutersMode
    function_id: Optional[str] = ""

    class Settings:
        name = "sys-routers"


# functions


class DB_FUNCTION(Document):
    appid: str
    funcid: str
    description: Optional[str] = ""
    tag: Optional[List[str]] = []
    code: Optional[str] = ""
    createTime: datetime
    updateTime: datetime
    mode: str
    router: Optional[str] = None

    class Settings:
        name = "sys-functions"
