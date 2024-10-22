import secrets

from sqlalchemy import select
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import sessionmanager
from werkzeug.security import check_password_hash, generate_password_hash

from src.database import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_name(self, first_name: str, second_name: str) -> User | None:
        stmt = select(User).where(User.first_name == first_name, User.second_name == second_name).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email).limit(1)
        return await self.session.scalar(stmt)

    @staticmethod
    def compare_password(user_field: User, password: str) -> bool:
        old_password = user_field.password
        if old_password is None:
            old_password = ""
        return check_password_hash(old_password, password)

    async def get_by_auth(self, email: str, password: str) -> User | None:
        user_field = await self.get_by_email(email)
        if user_field is None:
            return None
        if not self.compare_password(user_field, password):
            return None
        return user_field

    async def set_first_name(self, user_field: User, first_name: str) -> bool:
        user_field = self.get_by_id(user_field.id)
        if user_field is None:
            return False
        user_field.first_name = first_name
        await self.session.flush()
        return True

    async def set_second_name(self, user_field: User, second_name: str) -> bool:
        user_field = self.get_by_id(user_field.id)
        if user_field is None:
            return False
        user_field.second_name = second_name
        await self.session.flush()
        return True

    async def set_password(self, user_field: User, new_password: str) -> None:
        user_field.password = generate_password_hash(new_password)
        user_field.secret = secrets.token_urlsafe(8)
        await self.session.flush()

    async def registration(self, email: str, password: str) -> User | None:
        user_field = User(email=email)
        self.session.add(user_field)
        await self.set_password(user_field, password)
        return await self.get_by_id(user_field.id)
