from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from app.dto.model.base import Base
from app.dto.model.mixins import TimeMixin


class User(TimeMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    birth = mapped_column(Date)
    sex: Mapped[str]
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)
