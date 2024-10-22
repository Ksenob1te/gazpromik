from pydantic import BaseModel
from uuid import UUID

from . import UserScheme
from typing import List


class CompanyScheme(BaseModel):
    id: UUID
    name: str
    users: List[UserScheme]

    class Config:
        orm_mode = True