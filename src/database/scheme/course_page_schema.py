from pydantic import BaseModel

from . import CourseScheme

class CoursePageScheme(BaseModel):
    id: int
    course_id: int
    page_number: int

    class Config:
        orm_mode = True