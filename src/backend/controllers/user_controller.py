from typing import Optional
from datetime import timedelta

from fastapi import Depends, Response
from fastapi_controllers import Controller, get, post
from pydantic import BaseModel

from src.database import get_db_session
from src.database import User
from src.service import UserService
from src.database.scheme import UserScheme
from src.backend import manager
import json


class InfoResponse(BaseModel):
    auth: bool
    profile: Optional[UserScheme]

    class Config:
        orm_mode = True


class UserController(Controller):
    prefix = "/user"
    tags = ["user"]

    def __init__(self, session=Depends(get_db_session)):
        self.session = session
        self.user_service = UserService(session)

    @get("/", response_model=InfoResponse)
    async def getInfo(self, user_field: User | None = Depends(manager.optional)):
        response = {"auth": user_field is not None,
                    "profile": user_field}
        return response


class LoginRequest(BaseModel):
    email: str
    password: str
    remember_me: bool


class RegistrationRequest(BaseModel):
    email: str
    password: str
    password_again: str


class AuthController(Controller):
    prefix = "/auth"
    tags = ["auth"]

    def __init__(self, session=Depends(get_db_session)):
        self.session = session
        self.user_service = UserService(session)

    @post("/login")
    async def login(self, response: Response, request: LoginRequest):
        user = await self.user_service.login(request.email, request.password)
        user = {"ID": str(user.id), "Secret": user.secret}
        access_token = manager.create_access_token(
            data=dict(sub=json.dumps(user)),
            expires=timedelta(
                days=30) if request.remember_me else timedelta(days=1)
        )
        response.set_cookie("access-token", access_token, max_age=60 *
                                                                  60 * 24 * 30 if request.remember_me else 60 * 60 * 24,
                            httponly=True)
        return {"message": "OK"}

    @post("/registration")
    async def registration(self, request: RegistrationRequest):
        await self.user_service.registration(request.email, request.password, request.password_again)
        await self.session.commit()
        return {"message": "OK"}

    @get("/logout")
    def logout(self, response: Response, profile: User | None = Depends(manager)):
        response.set_cookie("access-token", "", max_age=0, httponly=True)
        response.set_cookie("workspace", "", max_age=0)
        return {"message": "OK"}