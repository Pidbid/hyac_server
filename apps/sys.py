# -*- encoding: utf-8 -*-
"""
@File    :   sys.py
@Time    :   2023/08/23 02:59:45
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   这里输入一些文件介绍
"""

# here put the import lib
from fastapi import APIRouter

# from models.db import DB

# from apps.db.database import sys_database
from apps.user import user

from apps.application import sys_apps

from apps.router import sys_router

from apps.function import sys_function

# db = DB()
sys_services = APIRouter()

# 文档操作操作
# sys_services.include_router(sys_database, prefix="/database")

# user api
sys_services.include_router(user, prefix="/user")

# application api
sys_services.include_router(sys_apps, prefix="/apps")

# router api
sys_services.include_router(sys_router, prefix="/router")

# setting api
# sys_services.include_router(sys_config,prefix="/config")

# function api
sys_services.include_router(sys_function, prefix="/func")
