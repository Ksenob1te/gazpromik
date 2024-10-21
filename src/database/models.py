from typing import Optional

from sqlalchemy import JSON
from uuid import uuid4, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, DateTime
from . import Base
from typing import List
import datetime


company_user_table = Table(
    "company_user_table",
    Base.metadata,
    Column("user_id", ForeignKey("user_table.id"), primary_key=True),
    Column("company_id", ForeignKey("company_table.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    first_name: Mapped[str]
    second_name: Mapped[str]
    password: Mapped[str | None]
    secret: Mapped[str | None]
    companies: Mapped[List["Company"]] = relationship(secondary=company_user_table, back_populates="users", lazy='selectin')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, first_name={self.first_name!r}, second_name={self.second_name!r})"


class Company(Base):
    __tablename__ = "company_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    users: Mapped[List["User"]] = relationship(secondary=company_user_table, back_populates="companies", lazy='selectin')

    def __repr__(self) -> str:
        return f"Company(id={self.id!r}, name={self.name!r})"


class Course(Base):
    __tablename__ = "course_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int] = mapped_column(default=10000)
    company_id: Mapped[int] = mapped_column(ForeignKey("company_table.id"))
    company: Mapped[Company] = relationship("Company", back_populates="courses")

    def __repr__(self) -> str:
        return f"Course(id={self.id!r}, name={self.name!r}, description={self.description!r})"


class UserCourse(Base):
    __tablename__ = "user_course_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"))
    course_id: Mapped[UUID] = mapped_column(ForeignKey("course_table.id"))

    user: Mapped[User] = relationship(lazy='selectin')
    course: Mapped[Course] = relationship(lazy='selectin')

    status: Mapped[str] = mapped_column(default="not_started")
    score: Mapped[int] = mapped_column(default=0)
    is_complete: Mapped[bool] = mapped_column(default=False)
    completion_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return f"UserCourse(id={self.id!r}, user={self.user_id!r}, course={self.course_id!r})"


class PrerequisiteAccess(Base):
    __tablename__ = "prerequisite_access_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    course_id: Mapped[UUID] = mapped_column(ForeignKey("course_table.id"))
    prerequisite_id: Mapped[UUID] = mapped_column(ForeignKey("course_table.id"))

    course: Mapped[Course] = relationship(lazy='selectin')
    prerequisite: Mapped[Course] = relationship(lazy='selectin')

    free_threshold: Mapped[int] = mapped_column(default=0)

    def __repr__(self) -> str:
        return f"PrerequisiteAccess(id={self.id!r}, course={self.course_id!r}, prerequisite={self.prerequisite_id!r})"


class UserAccess(Base):
    __tablename__ = "user_access_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"))
    course_id: Mapped[UUID] = mapped_column(ForeignKey("course_table.id"))

    user: Mapped[User] = relationship(lazy='selectin')
    course: Mapped[Course] = relationship(lazy='selectin')

    is_free: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"UserAccess(id={self.id!r}, user={self.user_id!r}, course={self.course_id!r})"


class CoursePage(Base):
    __tablename__ = "course_page_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    course_id: Mapped[UUID] = mapped_column(ForeignKey("course_table.id"))
    course: Mapped[Course] = relationship(lazy='selectin')
    page_number: Mapped[int] = mapped_column(default=0)

    def __repr__(self) -> str:
        return f"CoursePage(id={self.id!r}, course={self.course_id!r}, page_number={self.page_number!r}"


class Block(Base):
    __tablename__ = "block_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    course_page_id: Mapped[UUID] = mapped_column(ForeignKey("course_page_table.id"))
    course_page: Mapped[CoursePage] = relationship(lazy='selectin')
    title: Mapped[str]
    block_position: Mapped[int] = mapped_column(default=0)

    def __repr__(self) -> str:
        return f"Block(id={self.id!r}, course_page={self.course_page_id!r}, title={self.title!r}"

class Element(Base):
    __tablename__ = "element_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    block_id: Mapped[UUID] = mapped_column(ForeignKey("block_table.id"))
    block: Mapped[Block] = relationship(lazy='selectin')
    element_type: Mapped[str]

    def __repr__(self) -> str:
        return f"Element(id={self.id!r}, block={self.block_id!r}, element_type={self.element_type!r}"


class Splitter(Base):
    __tablename__ = "splitter_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    element_id: Mapped[UUID] = mapped_column(ForeignKey("element_table.id"))
    element: Mapped[Element] = relationship(lazy='selectin')

    def __repr__(self) -> str:
        return f"Splitter(id={self.id!r}, element={self.element_id!r}"


class Image(Base):
    __tablename__ = "image_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    element_id: Mapped[UUID] = mapped_column(ForeignKey("element_table.id"))
    element: Mapped[Element] = relationship(lazy='selectin')
    image_src: Mapped[str]

    def __repr__(self) -> str:
        return f"Image(id={self.id!r}, element={self.element_id!r}, image_url={self.image_src!r}"


class Video(Base):
    __tablename__ = "video_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    element_id: Mapped[UUID] = mapped_column(ForeignKey("element_table.id"))
    element: Mapped[Element] = relationship(lazy='selectin')
    video_src: Mapped[str]

    def __repr__(self) -> str:
        return f"Video(id={self.id!r}, element={self.element_id!r}, video_url={self.video_src!r}"


class Text(Base):
    __tablename__ = "text_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    element_id: Mapped[UUID] = mapped_column(ForeignKey("element_table.id"))
    element: Mapped[Element] = relationship(lazy='selectin')
    text: Mapped[str]

    def __repr__(self) -> str:
        return f"Text(id={self.id!r}, element={self.element_id!r}, text={self.text!r}"


class Question(Base):
    __tablename__ = "question_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    element_id: Mapped[UUID] = mapped_column(ForeignKey("element_table.id"))
    element: Mapped[Element] = relationship(lazy='selectin')
    question: Mapped[str]

    def __repr__(self) -> str:
        return f"Question(id={self.id!r}, element={self.element_id!r}, question={self.question!r}"


class Audio(Base):
    __tablename__ = "audio_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    element_id: Mapped[UUID] = mapped_column(ForeignKey("element_table.id"))
    element: Mapped[Element] = relationship(lazy='selectin')
    audio_src: Mapped[str]

    def __repr__(self) -> str:
        return f"Audio(id={self.id!r}, element={self.element_id!r}, audio_url={self.audio_src!r}"


class Answer(Base):
    __tablename__ = "answer_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    question_id: Mapped[UUID] = mapped_column(ForeignKey("question_table.id"))
    question: Mapped[Question] = relationship(lazy='selectin')
    answer_type: Mapped[str]
    title: Mapped[str]

    def __repr__(self) -> str:
        return f"Answer(id={self.id!r}, question={self.question_id!r}, title={self.title!r}"


class AnswerSelect(Base):
    __tablename__ = "answer_select_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    answer_id: Mapped[UUID] = mapped_column(ForeignKey("answer_table.id"))
    answer: Mapped[Answer] = relationship(lazy='selectin')
    is_answer: Mapped[bool] = mapped_column(default=False)
    title: Mapped[str]

    def __repr__(self) -> str:
        return f"AnswerSelect(id={self.id!r}, answer={self.answer_id!r}, title={self.title!r}"


class AnswerText(Base):
    __tablename__ = "answer_text_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    answer_id: Mapped[UUID] = mapped_column(ForeignKey("answer_table.id"))
    answer: Mapped[Answer] = relationship(lazy='selectin')
    ethalon_answer: Mapped[str]
    title: Mapped[str]

    def __repr__(self) -> str:
        return f"AnswerText(id={self.id!r}, answer={self.answer_id!r}, title={self.title!r}"


class Payments(Base):
    __tablename__ = "payments_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"))
    user: Mapped[User] = relationship(lazy='selectin')
    course_id: Mapped[UUID] = mapped_column(ForeignKey("course_table.id"))
    course: Mapped[Course] = relationship(lazy='selectin')
    payment_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return f"Payments(id={self.id!r}, user={self.user_id!r}, course={self.course_id!r}"
