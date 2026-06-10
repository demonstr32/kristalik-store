from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.cart import CartItemResponseSchema, CartItemSchema, CartItemUpdateSchema, CartResponseSchema
from app.models.user import UserORM
from app.services.cart import  CartService, ItemNotFound, NotUserCart
from app.api.dependencies import get_cart_service, get_current_user

router = APIRouter(prefix="/cart")
@router.get("",status_code=status.HTTP_200_OK)
def read_cart(current_user: UserORM = Depends(get_current_user),cart_service: CartService = Depends(get_cart_service))->CartResponseSchema:
    return cart_service.get_cart(current_user.id)

@router.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(payload: CartItemSchema, current_user: UserORM = Depends(get_current_user),cart_service: CartService = Depends(get_cart_service))->CartItemResponseSchema:
    try:
        return cart_service.add_item(current_user.id,payload)
    except ItemNotFound as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=str(e))
@router.patch("/items/{item_id}")
def update_item(item_id: int,payload: CartItemUpdateSchema,current_user: UserORM = Depends(get_current_user),cart_service: CartService = Depends(get_cart_service))->CartItemResponseSchema:
    try:
        return cart_service.update_item(current_user.id,item_id,payload)
    except ItemNotFound as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=str(e))
    except NotUserCart as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=str(e))
@router.delete("/items/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
def del_item(item_id: int,current_user: UserORM = Depends(get_current_user),cart_service: CartService = Depends(get_cart_service))->None:
    try:
        cart_service.remove_item(current_user.id,item_id)
    except ItemNotFound as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=str(e))
    except NotUserCart as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=str(e))
@router.delete("",status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(current_user: UserORM = Depends(get_current_user),cart_service: CartService = Depends(get_cart_service))->None:
    cart_service.clear_cart(current_user.id)
    
