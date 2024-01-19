from fastapi import APIRouter, Depends
from schemas.product_schemas import ProductCreate
from repository.data_service.product_repo import create_product, get_product, get_product_by_name, update_product, delete_product
from helper.response import post_data_fail, success_post_data, success_get_data, get_data_null
from helper.jwt import jwt_exist, isNotUser

goods = APIRouter(prefix="/good", tags=["PRODUCT Detail"])

@goods.get("/", summary="get all product", dependencies=[Depends(jwt_exist)])
async def get_all_goods():
    data = get_product()
    if data:
        return success_get_data(data)
    return get_data_null("Product Not Found")

@goods.get("/{name}", summary="get product by name", dependencies=[Depends(jwt_exist)])
async def get_product_name(name: str):
    data = get_product_by_name(name)
    if data:
        return success_get_data(data)
    return get_data_null(f"product with {name} not found")

@goods.post("/create_product", summary="Create Product, only admin and superadmin can create product", dependencies=[Depends(isNotUser)])
async def create_goods(product: ProductCreate):
    try:
        createData = create_product(product)
        if createData:
            return success_post_data(200, 1, "Success Create Product")
        return post_data_fail("create data fail")
    except Exception as e:
        return post_data_fail(f"error post data: {str(e)}")

@goods.put("/update/{id_product}", summary="update product by id_product", dependencies=[Depends(isNotUser)])
async def update(id_product:int, product: ProductCreate):
    try:
        update = update_product(id_product, product)
        if update:
            return success_post_data(200, 1, "success update data product")
        return post_data_fail("failure update data")
    except Exception as e:
        return post_data_fail(f"Error Update data: {str(e)}")

@goods.delete("/delete/{id_product}", summary="Deleted product, only admin and superadmin can delete", dependencies=[Depends(isNotUser)])
async def deleted(id_product:int):
    try:
        deleted = delete_product(id_product)
        if deleted:
            return success_post_data(200, 1, "deleted product success")
        
        return post_data_fail("failure delete data")
    except Exception as e:
        return post_data_fail(f"Error deleted data: {str(e)}")