from sqlalchemy.orm import Mapped, mapped_column

from app.dto.model.base import Base
from app.dto.model.mixins import TimeMixin


class User(Base, TimeMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)