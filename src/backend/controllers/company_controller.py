from fastapi import Depends, Response, HTTPException
from fastapi_controllers import Controller, get, post
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session
from src.database import User
from src.database.scheme import CompanyScheme, UserScheme
from src.service import CompanyService, UserService
from ..login_manager import manager
from starlette.status import HTTP_403_FORBIDDEN
from uuid import UUID


class CreateOrganisationRequest(BaseModel):
    name: str


class KickRequest(BaseModel):
    user_id: int


class SetRepoRequest(BaseModel):
    repo_name: str


class CompanyController(Controller):
    prefix = "/company"
    tags = ["company"]

    def __init__(self,
                 session: AsyncSession = Depends(get_db_session),
                 user: User = Depends(manager)) -> None:
        self.session = session
        self.user = user

        self.company_service = CompanyService(session)
        self.user_service = UserService(session)

    @post("/", response_model=CompanyScheme)
    async def create_organisation(self, request: CreateOrganisationRequest):
        user = await self.user_service.get_by_id(self.user.id)
        organisation = await self.company_service.create(user, request.name)
        await self.session.commit()
        return organisation

    @post("/{organisation_id}/leave")
    async def organisation_leave(self, company_id: UUID):
        user = await self.user_service.get_by_id(self.user.id)
        organisation = await self.company_service.get_by_id(company_id)
        await self.company_service.check_participant(organisation, user)
        await self.company_service.remove_user(organisation, user)
        await self.session.commit()
        return {"message": "OK"}

    @get("/{organisation_id}/members", response_model=list[UserScheme])
    async def get_organisation_members(self, company_id: UUID):
        organisation = await self.company_service.get_by_id(company_id)
        await self.company_service.check_participant(organisation, self.user)
        return await self.company_service.get_users(organisation)