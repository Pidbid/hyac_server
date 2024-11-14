# -*- encoding: utf-8 -*-
"""
@File    :   token.py
@Time    :   2023/01/08 18:50:47
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   JWT token
"""

# here put the import lib
import jwt
import time
from models.config import CONFIG

config = CONFIG()


class TOKEN:
    def __init__(self) -> None:
        self.salt = config.token_salt
        self.headers = {"alg": "HS256", "typ": "JWT"}

    def create(self, data: dict):
        exp = int(time.time()) + 12 * 60 * 60
        data.update({"exp": exp})
        token = jwt.encode(
            payload=data, key=self.salt, algorithm="HS256", headers=self.headers
        )
        return {"token": token, "tokenExpired": exp}

    def verify(self, token: str):
        # try:
        #     info = jwt.decode(token, self.salt, True, algorithm="HS256")
        #     if int(time.time()) > info["jwt"]:
        #         return False
        #     else:
        #         return info
        # except:
        #     return False
        try:
            info = jwt.decode(
                token, self.salt, algorithms=["HS256"], headers=self.headers
            )
            return info
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("The token has expired", token)
        except jwt.InvalidTokenError:
            return False
