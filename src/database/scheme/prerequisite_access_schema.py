from pydantic import BaseModel

from . import CourseScheme

class PrerequisiteAccessScheme(BaseModel):
    id: int
    course: CourseScheme
    prerequisite: CourseScheme
    free_threshold: int

    class Config:
        orm_mode = True