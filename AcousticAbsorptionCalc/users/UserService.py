import hashlib
from typing import Optional
from users.models import User  

class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
