# -*- encoding: utf-8 -*-
"""
@File    :   etcd_test.py
@Time    :   2024/11/14 21:11:38
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   这里输入一些文件介绍
"""

# here put the import lib
from models.etcd import HY_ETCD

etcd = HY_ETCD()
etcd.put("a", 123)
