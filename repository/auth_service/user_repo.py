import bcrypt
from config.db_connection import db_conn
from schemas.user_schemas import CreateUser, Register, Login, ForgotPw
from model.user_model import UserMdl


def get_users() -> list:
    conn = db_conn()
    data = conn.query(UserMdl).all()
    serialized_users = [{"id_user": user.id_user, "full_name": user.full_name, "username": user.username,
                             "email": user.email, "user_level": user.user_level} for user in data]
    return serialized_users

def check_username(username: str) -> bool:
    conn = db_conn()
    isUsernameExist = conn.query(UserMdl).filter_by(username=username).first()
    if isUsernameExist:
        return False
    
    return True

def check_email(email: str) -> bool:
    conn = db_conn()
    isEmailExist = conn.query(UserMdl).filter_by(email=email).first()
    if isEmailExist:
        return False
    return True

def hashPassword(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def check_password(password: str, hashed_password: str) -> bool :
    stringEncode = password.encode('utf-8')
    isMatch = bcrypt.checkpw(stringEncode, hashed_password)
    return isMatch

def registerUser(user: Register) -> bool:
    conn = db_conn()
    if user.password == user.confirm_password:
        passwordHash = hashPassword(user.password)
        data = UserMdl(
            full_name=user.full_name,
            username=user.username,
            email=user.email,
            password=passwordHash,
        )
        conn.add(data)
        conn.commit()
        conn.refresh(data)
        return True
    return False

def createUser(user: CreateUser) -> bool:
    conn = db_conn()
    if user.password == user.confirm_password:
        passwordHash = hashPassword(user.password)
        data = UserMdl(
            full_name=user.full_name,
            username=user.username,
            email=user.email,
            password=passwordHash,
            user_level=user.level
        )
        conn.add(data)
        conn.commit()
        conn.refresh(data)
        return True
    return False
def login(userData: Login) -> dict:
    conn = db_conn()
    dataUser = conn.query(UserMdl).filter_by(username=userData.username).first()
    result = {}
    if dataUser:
        verifyPassword = check_password(userData.password, dataUser.password.encode('utf-8'))
        if verifyPassword:
            result = {
                'username': dataUser.username,
                'full_name': dataUser.full_name,
                'email': dataUser.email,
                'level': dataUser.user_level,
                'message': None
            }
        else:
            result = {
                "message": "invalid password"
            }
    else:
        result = {
            "message": "invalid username"
        }
    
    return result

def update_password(user: ForgotPw) -> bool:
    conn = db_conn()
    userData = conn.query(UserMdl).filter_by(username=user.username, email=user.email).first()
    if userData:
        userData.password = hashPassword(user.password)
        conn.commit()
        return True
    return False

def delete_user(username: str) -> bool :
    conn = db_conn()
    data = conn.query(UserMdl).filter_by(username=username).first()
    if data:
        conn.delete(data)
        conn.commit()
        return True
    return False