# -*- encoding: utf-8 -*-
"""
@File    :   middleware.py
@Time    :   2024/11/14 00:49:52
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
@Desc    :   fastapi middleware
"""

# here put the import lib
from fastapi import HTTPException, status, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# from starlette.requests import Request

from models.token import TOKEN
from models.config import CONFIG

config = CONFIG()


class MwJwttoken(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path in config.unauth_routers:
            return await call_next(request)
        authorization = request.headers.get("Authorization")
        if not authorization:
            return Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content="Not Authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            token = TOKEN()
            token_res = token.verify(authorization.split()[1])
            if not token_res:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            request.state.tokeninfo = token_res
        response = await call_next(request)
        return response
