import orjson as json
import datetime
from fastapi import Depends, HTTPException
from fastapi_another_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer

class CustomHTTPBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, scheme_name: str = None, scopes: dict = None):
        super().__init__(auto_error=auto_error, scheme_name=scheme_name)
        self.scopes = scopes

def create_access_token(Authorize: AuthJWT, data: dict) -> str:
    return Authorize.create_access_token(
        subject=json.dumps(
            data
        ).decode('utf-8'),
        expires_time=datetime.timedelta(days=1)
    )

def create_refresh_token(Authorize: AuthJWT, data: dict) -> str:
    return Authorize.create_access_token(
        subject=json.dumps(
            data
        ).decode('utf-8'),
        expires_time=datetime.timedelta(days=7)
    )

def check_jwt_exist(Authorize: AuthJWT) -> bool :
    Authorize.jwt_required()
    return True

def isSuperAdmin(Authorize: AuthJWT = Depends(), bearer: str = Depends(CustomHTTPBearer())) -> bool:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    userData = json.loads(current_user)
    if 'level' in userData and userData["level"] == '0':
        return True
    else:
        raise HTTPException(status_code=403, detail="You do not have access to this resource as a superadmin")
    
def isNotUser(Authorize: AuthJWT = Depends(), bearer: str = Depends(CustomHTTPBearer())) -> bool:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    userData = json.loads(current_user)
    if 'level' in userData and userData["level"] != '2':
        return True
    else:
        raise HTTPException(status_code=403, detail="You do not have access to this resource as a superadmin and admin")
    
def jwt_exist(Authorize: AuthJWT = Depends(), bearer: str = Depends(CustomHTTPBearer())) -> bool:
    Authorize.jwt_required()
    return True