from pydantic import BaseModel

class BlockScheme(BaseModel):
    id: int
    course_page_id: int
    title: str
    block_position: int

    class Config:
        orm_mode = True