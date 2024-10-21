from pydantic import BaseModel

class ImageScheme(BaseModel):
    id: int
    element_id: int
    image_src: str

    class Config:
        orm_mode = True


class VideoScheme(BaseModel):
    id: int
    element_id: int
    video_src: str

    class Config:
        orm_mode = True


class TextScheme(BaseModel):
    id: int
    element_id: int
    text: str

    class Config:
        orm_mode = True


class QuestionScheme(BaseModel):
    id: int
    element_id: int
    question: str

    class Config:
        orm_mode = True


class AudioScheme(BaseModel):
    id: int
    element_id: int
    audio_src: str

    class Config:
        orm_mode = True
