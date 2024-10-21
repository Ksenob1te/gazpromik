from fastapi import HTTPException
from sqlalchemy.util import await_only

from database import sessionmanager
from src.database import User
from src.database import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
# TODO: install fastapi_login
# from fastapi_login.exceptions import InvalidCredentialsException
from starlette.status import HTTP_400_BAD_REQUEST


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.user_repository = UserRepository(session)

    async def login(self, email: str, password: str) -> User:
        """
        :raises InvalidCredentialsException: if user is not registered
        :param email: str
        :param password: str
        :return: user field
        """
        user_field = await self.user_repository.get_by_auth(email=email, password=password)
        if user_field is None:
            # TODO: here change the exception after fastapi_login installation
            # raise InvalidCredentialsException
            raise Exception("InvalidCredentials")
        return user_field

    @staticmethod
    async def get_full_name(user_field: User) -> str:
        full_name: str = ""
        if user_field.first_name is not None:
            full_name += user_field.first_name
            if user_field.second_name is not None:
                full_name += " "
        if user_field.second_name is not None:
            full_name += user_field.second_name
        return full_name

    async def registration(self, email: str, password: str, repeat_password: str) -> User | None:
        """
        Method for user registration in the system

        :raise HTTP_400_BAD_REQUEST: if user with email already exists or passwords doesn't match
        :param email: str
        :param password: str
        :param repeat_password: str
        :return: user field or None
        """
        if password != repeat_password:
            raise HTTPException(HTTP_400_BAD_REQUEST, "Passwords don't match")

        if await self.user_repository.get_by_email(email=email):
            raise HTTPException(HTTP_400_BAD_REQUEST, "User already exists")

        return await self.user_repository.registration(email, password)

    async def set_first_name(self, user_field: User, new_first_name: str) -> None:
        if not await self.user_repository.set_first_name(user_field, new_first_name):
            raise HTTPException(HTTP_400_BAD_REQUEST, "Unable to set user's first name")

    async def set_second_name(self, user_field: User, new_second_name: str) -> None:
        if not await self.user_repository.set_second_name(user_field, new_second_name):
            raise HTTPException(HTTP_400_BAD_REQUEST, "Unable to set user's second name")


