from pydantic import BaseModel

from . import CompanyScheme

class CourseScheme(BaseModel):
    id: int
    name: str
    description: str
    price: int
    company: CompanyScheme

    class Config:
        orm_mode = True