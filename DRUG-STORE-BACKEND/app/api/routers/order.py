from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.order import OrderORM
from app.models.order_item import OrderItemORM
from app.models.user import UserORM
from app.schemas.order import  OrderUpdateSchema, OrderResponseSchema
from app.api.dependencies import get_current_user, get_is_admin, get_order_service
from app.services.order import OrderService, OrderCannotBeCancelled, NotUserOrder, OrderNotFound,NoCartItem,NoProduct

router = APIRouter(prefix="/orders")

@router.post("",status_code=status.HTTP_201_CREATED)
def create_order(current_user: UserORM = Depends(get_current_user),order_service: OrderService = Depends(get_order_service))->OrderResponseSchema:
    try:
        return order_service.create_order(current_user.user_id)
    except NoCartItem as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = str(e))
    except NoProduct as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = str(e))

@router.get("",status_code = status.HTTP_200_OK)
def get_orders(current_user:  UserORM = Depends(get_current_user),order_service: OrderService = Depends(get_order_service))->list[OrderResponseSchema]:
    return order_service.get_user_orders(current_user.user_id)
@router.get("/{order_id}",status_code = status.HTTP_200_OK)
def get_order(order_id: UUID,current_user:  UserORM = Depends(get_current_user),order_service: OrderService = Depends(get_order_service))->OrderResponseSchema:
    try:
        return order_service.get_order(order_id,current_user.user_id)
    except OrderNotFound as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = str(e))
    except NotUserOrder as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = str(e))
@router.post("/{order_id}/cancel",status_code=status.HTTP_200_OK)
def cancel_order(order_id: UUID, current_user:  UserORM = Depends(get_current_user),order_service: OrderService = Depends(get_order_service))->OrderResponseSchema:
    try:
        return order_service.cancel_order(order_id,current_user.user_id)
    except OrderNotFound as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = str(e))
    except NotUserOrder as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = str(e))
    except OrderCannotBeCancelled as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = str(e))
@router.patch("/admin/{order_id}/status")
def update_status(order_id: UUID,status: OrderUpdateSchema, is_admin: bool = Depends(get_is_admin),order_service: OrderService = Depends(get_order_service))->OrderResponseSchema:
    try:
        return order_service.update_order_status(order_id,status.status)
    except OrderNotFound as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = str(e))
@router.delete("/{order_id}",status_code=status.HTTP_204_NO_CONTENT)
def del_order(order_id: UUID, is_admin: bool = Depends(get_is_admin),order_service: OrderService = Depends(get_order_service))->None:
    order_service.delete_order(order_id)