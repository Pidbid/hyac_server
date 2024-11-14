# -*- encoding: utf-8 -*-
"""
@File    :   passwords.py
@Time    :   2023/01/09 19:34:12
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   密码相关操作
"""

# here put the import lib
import hashlib
import random


def generate_rand_str(
    length: str = 8, hasNumbers: bool = True, hasSymbols: bool = False
):
    alpha = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    numbers = "0123456789"
    symbols = "!@#$%^&*_-=+"
    charts = alpha
    if hasNumbers:
        charts += numbers
    if hasSymbols:
        charts += symbols
    rand_str = ""
    for i in range(length):
        rand_str += random.choice(charts)
    return rand_str


def hash_password(context: str):
    hash_sha256 = hashlib.sha256()
    hash_sha256.update(context.encode("utf-8"))
    return hash_sha256.hexdigest()


def hash_function_code(code: str):
    hash_md5 = hashlib.md5()
    hash_md5.update(code.encode("utf-8"))
    return hash_md5.hexdigest()
