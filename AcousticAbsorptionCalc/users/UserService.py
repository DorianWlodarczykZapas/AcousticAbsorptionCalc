import hashlib
from typing import Optional
from users.models import User  

class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    
    def register_user(self, username: str, email: str, password: str, role: str = "user") -> User:
        password_hash = self.hash_password(password)
        user = User.objects.create(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )
        return user

    def login_user(self, email: str, password: str) -> Optional[User]:
        password_hash = self.hash_password(password)
        try:
            return User.objects.get(email=email, password_hash=password_hash)
        except User.DoesNotExist:
            return None
