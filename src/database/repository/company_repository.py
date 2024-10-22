import secrets
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import UUID

from database import company_user_table
from src.database import Company, User


class CompanyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> Optional[Company]:
        stmt = select(Company).where(Company.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_name(self, name: str) -> Optional[Company]:
        stmt = select(Company).where(Company.name == name).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, creator: User, name: str) -> Optional[Company]:
        organisation = Company(name=name)
        self.session.add(organisation)
        await self.session.flush()
        new_organisation = await self.get_by_id(organisation.id)
        new_organisation.users.append(creator)
        await self.session.flush()
        return new_organisation

    @staticmethod
    async def get_user_list(company_field: Company) -> list[User]:
        return company_field.users

    @staticmethod
    async def get_user_ids_list(company_field: Company) -> list[UUID]:
        return [i.id for i in list(company_field.users)]

    async def add_user(self, company: Company, user: User) -> None:
        if company not in user.companies:
            user.companies.append(company)
            await self.session.flush()

    async def remove_user(self, company: Company, user: User) -> None:
        if company in user.companies:
            user.companies.remove(company)
            await self.session.flush()
