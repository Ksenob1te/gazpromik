from pydantic import BaseModel

from . import CourseScheme, UserScheme

class UserAccessScheme(BaseModel):
    id: int
    course: CourseScheme
    user: UserScheme
    is_free: bool

    class Config:
        orm_mode = True