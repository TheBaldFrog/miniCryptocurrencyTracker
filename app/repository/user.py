from app.dto.model import User
from app.repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User
