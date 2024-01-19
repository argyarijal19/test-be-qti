from pydantic import BaseModel

class ProductCreate(BaseModel):
    productName: str
    productQty: int
    productDesc: str