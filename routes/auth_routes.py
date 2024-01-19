from fastapi import APIRouter, Depends
from fastapi_another_jwt_auth import AuthJWT
from schemas.user_schemas import Register, Login, CreateUser, ForgotPw
from repository.auth_service.user_repo import registerUser, check_email, check_username, login, update_password, delete_user, get_users
from helper.response import post_data_fail, success_post_data, success_get_data, get_data_null
from helper.jwt import create_access_token, isSuperAdmin, isNotUser

auth = APIRouter(prefix="/user", tags=["Authentication and USER Detail"])

@auth.get("/", summary="Get All User, only admin and superadmin can see all users", dependencies=[Depends(isNotUser)])
async def users():
    data = get_users()
    if data:
        result = []
        for user in data:
            result.append(user)
        return success_get_data(result)
    return get_data_null("users not found")
@auth.post("/login", summary="Login with username and password to get token")
async def login_routes(user: Login, authorize: AuthJWT = Depends()):
    dataUser = login(user)
    if dataUser["message"] == None:
        return {
            'token': create_access_token(
                Authorize=authorize,
                data={
                    'username': dataUser["username"],
                    'full_name': dataUser["full_name"],
                    'email': dataUser["email"],
                    'level': dataUser["level"],
                }
            ),
            'code': 200,
            'success': True,
            'message': 'Login Success'
        }
    else:
        return {
            'token': None,
            'code': 400,
            'success': False,
            'message': dataUser["message"]
        }


@auth.post("/register")
async def register_user(user: Register):
    try:
        if check_username(user.username):
            if check_email(user.email):
                if user.password == user.confirm_password:
                    reg = registerUser(user)
                    if reg:
                        print(reg)
                        return success_post_data(
                            201,
                            1,
                            "Register Success"
                        )
                    return post_data_fail("Register Failure")
                else:
                    return post_data_fail("Password Do not Match")
            else:
                return post_data_fail("Email is Already Registerd")
        else:
            return post_data_fail("Username is Already Registerd")
    except Exception as e:
        return post_data_fail(f"Register Failure: {e}")

@auth.post("/create_user", summary="Create User with Defined Level, only superadmin can defined level", dependencies=[Depends(isSuperAdmin)])
async def create_user_with_level(user: CreateUser):
    try:
        if check_username(user.username):
            if check_email(user.email):
                if user.password == user.confirm_password:
                    reg = registerUser(user)
                    if reg:
                        return success_post_data(
                            201,
                            1,
                            "Register Success"
                        )
                    return post_data_fail("Register Failure")
                else:
                    return post_data_fail("Password Do not Match")
            else:
                return post_data_fail("Email is Already Registerd")
        else:
            return post_data_fail("Username is Already Registerd")
    except Exception as e:
        return post_data_fail(f"Register Failure: {e}")

@auth.put("/update_pw", summary="update password when the user forgot")
async def forgot_password(user: ForgotPw):
    try:
        update = update_password(user)
        if update:
            return success_post_data(200, 1, "password has changed")
        return post_data_fail("fail change password, username or email invalid")
    except Exception as e:
        return post_data_fail(str(e))

@auth.delete("/delete_user/{username}", summary="Delete user by username, only super admin can delete user", dependencies=[Depends(isSuperAdmin)])
async def user_deleted(username: str):
    try:
        deleted = delete_user(username)
        if deleted:
            return success_post_data(200, 1, "success deleted user")
        return post_data_fail("delete failure, username not registered")
    except Exception as e:
        return post_data_fail(str(e))