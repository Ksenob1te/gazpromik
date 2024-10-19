from pydantic import BaseModel

from . import UserScheme, CourseScheme

class UserCourseScheme(BaseModel):
    id: int
    user: UserScheme
    course: CourseScheme
    status: str
    score: int
    is_complete: bool
    completion_date: str

    class Config:
        orm_mode = True