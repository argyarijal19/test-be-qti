from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProductMdl(Base):
    __tablename__ = "product"
    id_product = Column(Integer, primary_key=True)
    product_name = Column(String(30))
    product_qty = Column(Integer)
    product_description = Column(String(50))
