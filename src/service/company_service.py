from fastapi import HTTPException
from src.database import User, Company
from src.database import CompanyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN
from uuid import UUID


class CompanyService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.company_repository = CompanyRepository(session)

    async def create(self, creator: User, name: str) -> Company:
        organisation = await self.company_repository.create(creator, name)
        if organisation is None:
            raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, "Unable to create organisation")
        return organisation

    async def get_by_id(self, id: UUID) -> Company:
        organisation = await self.company_repository.get_by_id(id)
        if organisation is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "Organisation not found")
        return organisation

    async def get_users(self, company: Company) -> list[User]:
        return await self.company_repository.get_user_list(company)

    async def check_not_participant(self, company: Company, user: User) -> None:
        if user in await self.company_repository.get_user_ids_list(company):
            raise HTTPException(HTTP_403_FORBIDDEN, "Already participant")

    async def check_participant(self, company: Company, user: User) -> None:
        if user.id not in await self.company_repository.get_user_ids_list(company):
            raise HTTPException(HTTP_403_FORBIDDEN, "Not participant")

    async def add_user(self, company: Company, user: User) -> None:
        await self.company_repository.add_user(company, user)

    async def remove_user(self, company: Company, user: User) -> None:
        await self.company_repository.remove_user(company, user)


