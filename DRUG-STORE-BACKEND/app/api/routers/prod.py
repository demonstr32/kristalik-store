from fastapi import APIRouter, Depends, HTTPException, status
from app.services.prod import ProductService, ProductNotFound
from app.schemas.prod import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductResponseSchema
)
from app.api.dependencies import get_prod_service, get_is_admin

router = APIRouter(prefix="/products")
@router.get("",status_code=status.HTTP_200_OK)
async def read_products(prod_service: ProductService = Depends(get_prod_service))->list[ProductResponseSchema]:
    try:
        return await prod_service.list_prod()
    except ProductNotFound as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=str(e))

@router.get("/{prod_id}",status_code=status.HTTP_200_OK)
async def read_product(prod_id: int,prod_service: ProductService = Depends(get_prod_service))->ProductResponseSchema:
    try:
        return await prod_service.get_one_prod(prod_id=prod_id)
    except ProductNotFound as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=str(e))
@router.post("",status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreateSchema, is_admin: bool = Depends(get_is_admin), prod_service: ProductService = Depends(get_prod_service))->ProductResponseSchema:
    return await prod_service.create_prod(prod_create=payload)

@router.patch("/{prod_id}")
async def update_product(prod_id: int,payload: ProductUpdateSchema, is_admin: bool = Depends(get_is_admin), prod_service: ProductService = Depends(get_prod_service))->ProductResponseSchema:
    try:
        return await prod_service.update_prod(prod_id=prod_id,prod_update=payload)
    except ProductNotFound as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=str(e))
@router.delete("/{prod_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(prod_id: int,is_admin: bool = Depends(get_is_admin),prod_service: ProductService = Depends(get_prod_service))->None:
    try:
        await prod_service.delete_prod(prod_id=prod_id)
    except ProductNotFound as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=str(e))
