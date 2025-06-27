from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from src.core.db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, comment="user id")
    email: Mapped[str] = mapped_column(unique=True, nullable=False, comment="user email")
    password: Mapped[str] = mapped_column(nullable=False, comment="user password")
    name: Mapped[str] = mapped_column(nullable=False, comment="user name")
    last_name: Mapped[str] = mapped_column(nullable=False, comment="user last name")
    age: Mapped[int] = mapped_column(nullable=False, comment="user age")
    description: Mapped[str] = mapped_column(nullable=False, comment="user description")
    date_joined: Mapped[Optional[datetime]] = mapped_column(default=datetime.now, comment="user date joined")