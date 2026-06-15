from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import UserORM
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.prod import ProductService
from app.services.cart import CartService
from app.services.order import OrderService

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
)-> UserORM:
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = UserRepository(db).get_user_by_id(UUID(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
def get_is_admin(user: UserORM = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail="У вас нет прав на выполнение операции")
    return user.is_admin
def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)
def get_prod_service(db: Session = Depends(get_db)):
    return ProductService(db)
def get_cart_service(db: Session = Depends(get_db)):
    return CartService(db)
def get_order_service(db: Session = Depends(get_db)):
    return OrderService(db)
    