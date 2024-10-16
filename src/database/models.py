from typing import Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .engine import Base
from typing import List


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str | None]
    secret: Mapped[str | None]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"
