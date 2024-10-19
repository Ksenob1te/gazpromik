from pydantic import BaseModel

class UserScheme(BaseModel):
    id: int
    first_name: str
    second_name: str


    class Config:
        orm_mode = True