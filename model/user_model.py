from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserMdl(Base):
    __tablename__ = "users"
    id_user = Column(Integer, primary_key=True)
    full_name = Column(String(50))
    password = Column(String(350))
    username = Column(String(30))
    email = Column(String(50))
    user_level = Column(Enum('0', '1', '2'), default='2')
