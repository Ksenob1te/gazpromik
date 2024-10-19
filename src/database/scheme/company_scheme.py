from pydantic import BaseModel

from . import UserScheme
from typing import List


class CompanyScheme(BaseModel):
    id: int
    name: str
    users: List[UserScheme]

    class Config:
        orm_mode = True