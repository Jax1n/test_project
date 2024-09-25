from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import schemas

from . import models


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session):
    return db.query(models.Product).all()


def create_product(db: Session, product: schemas.Product):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: schemas.Product):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(db: Session):
    return db.query(models.Order).all()


def create_order(db: Session, order_items: list[schemas.OrderItem]):
    request_products = [i.product_id for i in order_items]
    db_products = db.query(models.Product).filter(models.Product.id.in_(request_products)).all()
    if len(db_products) != len(order_items):
        not_found_ids = set(request_products).difference(set([i.id for i in db_products]))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Products with id {not_found_ids} not found")
    tmp_dict = {i.product_id: i.product_count for i in order_items}
    for db_product in db_products:
        if db_product.count < tmp_dict[db_product.id]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product count with id {db_product.id} above then requested.")
        db_product.count -= tmp_dict[db_product.id]
    db_order = models.Order(status=schemas.OrderStatus.IN_PROCCESS)
    db.add(db_order)
    db.commit()
    db_order_items = [models.OrderItem(order_id=db_order.id, product_id=i.product_id, product_count=i.product_count) for i in order_items]
    db.add_all(db_order_items)
    db.commit()
    return db_order


def update_order(db: Session, order_id: int, request: schemas.OrderStatusUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        return None
    db_order.status = request.status
    db.commit()
    db.refresh(db_order)
    return db_order
