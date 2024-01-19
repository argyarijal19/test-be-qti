import uvicorn
import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from helper.exception import ExceptionHandler
from pydantic import BaseModel
from fastapi_another_jwt_auth import AuthJWT
from routes.auth_routes import auth
from routes.product_routes import goods

app = FastAPI()

ExceptionHandler(app=app)

class Settings(BaseModel):
    authjwt_secret_key: str
    authjwt_algorithm: str

@AuthJWT.load_config
def get_config():
    return Settings(
        authjwt_secret_key=os.getenv('secret'),
        authjwt_algorithm=os.getenv('algorithm')
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Backend - Test - For QTI",
        version="1.0.0",
        description="this Backend system is for fulfill your requirement task <br> Role User\n - super admin: '0'\n - admin : '1'\n - user : '2'\n <br> if the user doing registration role automated 2, if superadmin access create user, the superadmin can defined level ",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.include_router(auth)
app.include_router(goods)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)