
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .database import crud
from .dependencies import get_db
from .schemas import (
    OrderItem,
    OrderStatusUpdate,
    OrderWithItems,
    Product,
    ProductFull,
)

router = APIRouter()


@router.post("/products", response_model=ProductFull, status_code=status.HTTP_201_CREATED)
def create_product(request: Product, db: Session = Depends(get_db)):
    return crud.create_product(db, request)


@router.get("/products", response_model=list[ProductFull])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@router.get("/products/{id}", response_model=ProductFull)
def get_product(id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    return db_product


@router.put("/products/{id}", response_model=ProductFull)
def update_product(request: Product, id: int, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, id, request)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    return db_product


@router.delete("/products/{id}", response_model=dict)
def delete_product(id: int, db: Session = Depends(get_db)):
    is_success = crud.delete_product(db, id)
    if is_success is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    return Response(status_code=status.HTTP_200_OK)


@router.post("/orders", response_model=OrderWithItems, status_code=status.HTTP_201_CREATED)
def create_order(request: list[OrderItem], db: Session = Depends(get_db)):
    return crud.create_order(db, request)


@router.get("/orders", response_model=list[OrderWithItems])
def get_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)


@router.get("/orders/{id}", response_model=OrderWithItems)
def get_order(id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, id)
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
    return db_order


@router.patch("/orders/{id}/status", response_model=OrderWithItems)
def update_order_status(request: OrderStatusUpdate, id: int, db: Session = Depends(get_db)):
    db_order = crud.update_order(db, id, request)
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
    return db_order
