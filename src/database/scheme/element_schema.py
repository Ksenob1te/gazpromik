from pydantic import BaseModel

class ElementScheme(BaseModel):
    id: int
    block_id: int
    element_type: str

    class Config:
        orm_mode = True