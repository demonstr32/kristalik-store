from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.schemas.user import UserCreateSchema, UserResponseSchema, UserLoginSchema, UserUpdateSchema
from app.core.security import hash_password, verify_password, create_access_token

class UserAlreadyExists(Exception):
    """Пользователь уже существует"""

class UserNotFound(Exception):
    """Пользователь не найден"""

class InvalidPassword(Exception):
    """Неверный пароль"""
class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)
    
    def register_user(self, user_create: UserCreateSchema)-> UserResponseSchema:
        user_orm = self.user_repository.get_user_by_email(email=user_create.email)
        if user_orm:
            raise UserAlreadyExists(f"Пользователь с email: {user_create.email} уже существует")
        hashed_password = hash_password(user_create.password)
        user_orm = self.user_repository.create_user(email=user_create.email,hashed_password=hashed_password)
        self.db.commit()
        self.db.refresh(user_orm)
        return UserResponseSchema.model_validate(user_orm)
    
    def login_user(self, user_log: UserLoginSchema)->tuple[UserResponseSchema,str]:
        user_orm = self.user_repository.get_user_by_email(email=user_log.email)
        if not user_orm:
            raise UserNotFound(f"Пользователь с email: {user_log.email} не найден")
        if not verify_password(user_log.password, user_orm.hashed_password):
            raise InvalidPassword(f"Неверный пароль для пользователя: {user_log.email}")
        token = create_access_token(str(user_orm.user_id))
        return UserResponseSchema.model_validate(user_orm), token

    def update_user(self, user_id: str, user_update: UserUpdateSchema)-> UserResponseSchema:
        user_orm = self.user_repository.get_user_by_id(user_id=user_id)
        if not user_orm:
            raise UserNotFound(f"Пользователь с id: {user_id} не найден")
        if user_update.email:
            user_orm.email = user_update.email
        if user_update.password:
            user_orm.hashed_password = hash_password(user_update.password)
        self.db.commit()
        self.db.refresh(user_orm)
        return UserResponseSchema.model_validate(user_orm)
    
    def delete_user(self, user_id: str)->None:
        user_for_del = self.user_repository.get_user_by_id(user_id=user_id)
        if not user_for_del:
            raise UserNotFound(f"Пользователь с id: {user_id} не найден")
        self.user_repository.delete_user(user_for_del)
        self.db.commit()
        
