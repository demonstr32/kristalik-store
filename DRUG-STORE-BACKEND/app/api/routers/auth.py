from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth import AuthService, UserAlreadyExists, UserNotFound, InvalidPassword
from app.schemas.user import (
    UserCreateSchema,
    UserLoginSchema,
    UserResponseSchema,
    UserUpdateSchema,
    TokenResponseSchema,
)
from app.models.user import UserORM
from app.api.dependencies import get_auth_service, get_current_user  # get_is_admin не нужен здесь

router = APIRouter(prefix="/auth")

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    payload: UserCreateSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponseSchema:
    try:
        return auth_service.register_user(user_create=payload)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(
    payload: UserLoginSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponseSchema:
    try:
        user, token = auth_service.login_user(user_log=payload)
        return TokenResponseSchema(access_token=token, user=user)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidPassword as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.patch("/users/me", status_code=status.HTTP_200_OK)
def update_user(
    payload: UserUpdateSchema,
    current_user: UserORM = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponseSchema:
    try:
        return auth_service.update_user(user_id=current_user.id, user_update=payload)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    current_user: UserORM = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    try:
        auth_service.delete_user(user_id=current_user.id)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))