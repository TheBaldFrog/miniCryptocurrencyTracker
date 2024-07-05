from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import mapped_column

from app.dto.model.base import Base


class TimeMixin(Base):
    """Mxin to for datetime value of when the entity was created and when it was last modified."""

    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
