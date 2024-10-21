from pydantic import BaseModel

from . import QuestionScheme

class AnswerScheme(BaseModel):
    id: int
    question: QuestionScheme
    answer_type: str
    answer: str

    class Config:
        orm_mode = True

class AnswerSelectScheme(BaseModel):
    id: int
    title: str
    answer: AnswerScheme
    is_answer: bool

    class Config:
        orm_mode = True

class AnswerTextScheme(BaseModel):
    id: int
    title: str
    answer: AnswerScheme

    class Config:
        orm_mode = True