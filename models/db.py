# -*- encoding: utf-8 -*-
"""
@File    :   db.py
@Time    :   2023/08/23 02:58:44
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   mongodb handler
"""

# here put the import lib
from datetime import datetime
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from beanie import Document, Indexed, init_beanie
from beanie.odm.operators.update.general import Set
from models.config import CONFIG
from models.passwords import hash_password
from models.db_model import (
    DB_VERIFYCODE,
    DB_USER,
    DB_USER_LOGIN,
    DB_USER_NPW,
    DB_APPLICATION,
    DB_SETTING,
    DB_ROUTER,
    DB_FUNCTION,
)

config = CONFIG()


class DB:
    def __init__(self):
        self.client = AsyncIOMotorClient(
            "mongodb://{}:{}@{}:{}".format(
                config.db_sys_username,
                config.db_sys_password,
                config.db_sys_host,
                config.db_sys_port,
            )
        )
        self.db_model_rebuild()
        # await self.db_init()
        # Init beanie with the Product document class

    def db_model_rebuild(self):
        DB_VERIFYCODE.model_rebuild()
        DB_USER.model_rebuild()
        DB_USER_NPW.model_rebuild()

    async def db_init(self):
        # 初始化数据库
        await init_beanie(
            database=self.client.hyac,
            document_models=[
                DB_VERIFYCODE,
                DB_USER,
                DB_USER_LOGIN,
                DB_USER_NPW,
                DB_APPLICATION,
                DB_SETTING,
                DB_ROUTER,
                DB_FUNCTION,
            ],
        )

    async def __init_admin_account__(self):
        # add admin account
        admin_res = await DB_USER.find_one(DB_USER.username == config.username)
        if not admin_res:
            insert_res = await DB_USER(
                username=config.username,
                password=hash_password(config.password),
                createTime=datetime.now(),
                updateTime=datetime.now(),
                profile={"avatar": "", "nickName": config.username},
                roles=["admin"],
            ).insert()

    async def __init_settings__(self):
        # settings
        routers_setting = await DB_SETTING.find_one(DB_SETTING.mode == "unauth_routers")
        if not routers_setting:
            await DB_SETTING(
                mode="unauth_routers",
                description="unauthenticated routers",
                data=config.unauth_routers,
            ).insert()
        else:
            await routers_setting.update(
                {"$set": {DB_SETTING.data: config.unauth_routers}}
            )
