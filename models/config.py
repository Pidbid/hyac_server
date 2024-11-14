# -*- encoding: utf-8 -*-
"""
@File    :   config.py
@Time    :   2023/08/23 02:58:59
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   server config
"""

# here put the import lib
import os
from dotenv import find_dotenv, load_dotenv


class CONFIG:
    def __init__(self):
        self.load_env()
        self.env_list = os.environ
        self.db_sys()
        self.db_app()

    def load_env(self):
        load_dotenv(find_dotenv("./.env"), override=True)

    def db_sys(self):
        self.db_sys_host = self.env_list.get("DB_HOST")
        self.db_sys_port = self.env_list.get("DB_PORT")
        self.db_sys_username = self.env_list.get("DB_USERNAME")
        self.db_sys_password = self.env_list.get("DB_PASSWORD")
        self.token_salt = self.env_list.get("TOKEN_SALT")
        self.username = self.env_list.get("USERNAME")
        self.password = self.env_list.get("PASSWORD")
        self.unauth_routers = self.env_list.get("UNAUTH_ROUTERS")

    def db_app(self):
        pass
