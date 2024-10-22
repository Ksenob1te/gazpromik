from pydantic import BaseModel
from uuid import UUID


class UserScheme(BaseModel):
    id: UUID
    email: str
    first_name: str | None
    second_name: str | None

    class Config:
        orm_mode = True