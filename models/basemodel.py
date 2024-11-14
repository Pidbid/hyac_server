# -*- encoding: utf-8 -*-
"""
@File    :   basemodel.py
@Time    :   2023/01/08 18:46:57
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   基础类型定义
"""

# here put the import lib
from enum import Enum
from datetime import datetime
from typing import Union, Any, Optional, List, Dict, Literal
from pydantic import BaseModel, conlist, Field
from beanie import Document


class hyacResponse(BaseModel):
    code: int
    msg: str
    data: Union[int, str, Dict[str, Any], List[Any]] = None


class config(BaseModel):
    host: str


class userLogin(BaseModel):
    username: str
    password: str
    captcha: str


class userAdd(BaseModel):
    username: str
    password: str
    rules: list


class userLoginDate(BaseModel):
    login: int
    create: int


class userAddBase(BaseModel):
    username: str
    password: str
    nickname: str
    avatar: str
    login_ip: str
    date: userLoginDate


class dataBaseModel(BaseModel):
    page: int
    length: int


class addBaseModel(BaseModel):
    name: str
    data: Optional[Any] = None


class updateBaseModel(BaseModel):
    name: str
    data: Optional[Any] = None


class deleteBaseModel(BaseModel):
    name: str


class collectionAdd(BaseModel):
    pass


class applicationTypeModel(BaseModel):
    name: str
    spaceSize: int
    memorySize: int


class applicationCreateModel(BaseModel):
    name: str
    cpu: str
    memory: str


class applicationInfo(BaseModel):
    appid: str


class applicationRoute(BaseModel):
    appid: str


class initConfig(BaseModel):
    mode: str


class applicationFunData(BaseModel):
    appid: str
    page: int
    length: int


class functionInfo(BaseModel):
    """
    获取云函数的信息
    """

    appid: str
    functionid: str


class functionCreateModel(BaseModel):
    appid: str
    description: Optional[str] = ""
    tag: Optional[List[str]] = ""
    code: Optional[str] = ""
    mode: Optional[str] = ""


class functionUpdate(BaseModel):
    """
    函数更新
    """

    functionid: str
    data: dict


class userProfileModel(BaseModel):
    nickName: str
    avatar: Optional[str] = None
    email: Optional[str] = None


class dbApplicationStatus(str, Enum):
    creating = "creating"
    starting = "starting"
    running = "running"
    stopping = "stopping"
    stopped = "stopped"
    deleting = "deleting"
    deleted = "deleted"


class dbRoutersMode(str, Enum):
    router = "router"
    function = "function"


class applicationDeleteModel(BaseModel):
    appid: str


class applicationUpdateModel(BaseModel):
    appid: str
    cpu: Optional[str] = None
    memory: Optional[str] = None


class routerCreateModel(BaseModel):
    appid: str
    path: str
    parent_id: Optional[str] = None
    mode: Literal["router", "function"] = Field(
        ..., description="mode is router or function"
    )
    function_id: Optional[str] = None


class routerDeleteModel(BaseModel):
    id: str
