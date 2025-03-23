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

    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        try:
            user = User.objects.get(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.save()
            return user
        except User.DoesNotExist:
            return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return User.objects.filter(id=user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return User.objects.filter(email=email).first()


    def delete_user(self, user_id: int) -> bool:
        user = User.objects.filter(id=user_id).first()
        if user:
            user.delete()
            return True
        return False


