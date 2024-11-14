# -*- encoding: utf-8 -*-
"""
@File    :   verifycode.py
@Time    :   2023/01/10 03:11:18
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   verify code craete and verify
"""
# here put the import lib
import base64
import random
import time
from datetime import datetime, timedelta
from captcha.image import ImageCaptcha
from models.db_model import DB_VERIFYCODE
from beanie.operators import GTE


class VERIFYCODE:
    def __init__(self):
        pass

    async def create(self, length: int = 4) -> str:
        code = ""
        image = ImageCaptcha(width=160, height=60)
        for i in range(4):
            n = random.randint(0, 9)
            b = chr(random.randint(65, 90))
            s = chr(random.randint(97, 122))
            code += str(random.choice([n, b, s]))
        await DB_VERIFYCODE(
            code=code.lower(),
            expired=datetime.now() + timedelta(seconds=+300),
            scene="login",
        ).insert()
        img = image.generate(code)
        b64_image = base64.b64encode(img.read())
        return "data:image/png;base64," + str(b64_image, "utf-8")

    async def verify(self, code: str) -> bool:
        res_code = await DB_VERIFYCODE.find(
            {"code": code, "expired": {"$gte": datetime.now()}}
        ).to_list()
        if len(res_code) > 0:
            return True
        else:
            return False
