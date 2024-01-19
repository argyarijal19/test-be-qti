from config.db_connection import db_conn
from model.product_model import ProductMdl
from schemas.product_schemas import ProductCreate


def create_product(product: ProductCreate) -> bool:
    conn = db_conn()
    data = ProductMdl(
        product_name=product.productName,
        product_description=product.productDesc,
        product_qty=product.productQty
    )
    conn.add(data)
    conn.commit()
    return True

def get_product() -> list:
    conn = db_conn()
    data = conn.query(ProductMdl).all()
    if data:
        serialized_users = [{"product_name": good.product_name, "product_desc": good.product_description, "product_qty": good.product_qty, "id_product": good.id_product} for good in data]
        return serialized_users
    return []

def get_product_by_name(name:str) -> list:
    conn = db_conn()
    data = conn.query(ProductMdl).filter_by(product_name=name)
    if data:
        serialized_users = [{"product_name": good.product_name, "product_desc": good.product_description, "product_qty": good.product_qty, "id_product": good.id_product} for good in data]
        return serialized_users
    return []

def update_product(id_product:int, product: ProductCreate) -> bool: 
    conn = db_conn()
    data = conn.query(ProductMdl).filter_by(id_product=id_product).first()
    if data:
        data.product_description = product.productDesc
        data.product_name = product.productName
        data.product_qty = product.productQty
        conn.commit()
        return True
    return False

def delete_product(id_product: int) -> bool:
    conn = db_conn()
    data = conn.query(ProductMdl).filter_by(id_product=id_product).first()
    if data:
        conn.delete(data)
        conn.commit()
        return True
    return False


