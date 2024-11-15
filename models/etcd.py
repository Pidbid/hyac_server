# -*- encoding: utf-8 -*-
"""
@File    :   etcd.py
@Time    :   2024/11/16 02:01:04
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
"""

# here put the import lib
import etcd3
from models.config import CONFIG

config = CONFIG()


class ETCD:
    def __init__(self):
        self.etcd = etcd3.client(host="localhost", port=2379)

    def __db_init__(self):
        self.etcd.put("/server/db/password", config.db_sys_password)
