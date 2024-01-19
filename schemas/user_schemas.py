from pydantic import BaseModel, EmailStr, constr
from enum import Enum


class Register(BaseModel):
    full_name: str
    email: EmailStr
    username: str
    password: str
    confirm_password: str

class LevelEnum(str, Enum):
    user = '2'
    admin = '1'
    superAdmin = '0'

class CreateUser(BaseModel):
    full_name: str
    email: EmailStr
    username: str
    password: constr(min_length=6)
    confirm_password: constr(min_length=6)
    level: LevelEnum

class Login(BaseModel):
    username: str
    password: str

class ForgotPw(BaseModel):
    username: str
    email: EmailStr
    password: str