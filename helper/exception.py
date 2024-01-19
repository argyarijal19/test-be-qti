from fastapi import (
    FastAPI,
    status,
    HTTPException,
    Request
)
from fastapi.exceptions import (
    RequestValidationError
)
from fastapi.responses import ORJSONResponse as JSONResponse
from fastapi_another_jwt_auth.exceptions import (MissingTokenError, JWTDecodeError)


def ExceptionHandler(app: FastAPI) -> None :
    @app.exception_handler(RequestValidationError)
    async def http_validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={
                'code': status.HTTP_400_BAD_REQUEST,
                'success': False,
                'status': f'{exc.errors()[0]["msg"]} at {exc.errors()[0]["loc"][0]} need {exc.errors()[0]["loc"]} param',
                'data': None
            }
        )
    
    @app.exception_handler(JWTDecodeError)
    async def http_missing_token_exception_handler(request: Request, exc: JWTDecodeError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                'code': status.HTTP_401_UNAUTHORIZED,
                'success': False,
                'status': str(exc),
                'data': None
            }
        )
    
    @app.exception_handler(MissingTokenError)
    async def http_missing_token_exception_handler(request: Request, exc: MissingTokenError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'code': status.HTTP_400_BAD_REQUEST,
                'success': False,
                'status': exc.message,
                'data': None
            }
        )
    
    @app.exception_handler(Exception)
    async def http_internal_server_error_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'success': False,
                'status': str(exc),
                'data': None
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_jwt_unauthorized(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'code': exc.status_code,
                'success': False,
                'status': str(exc.detail),
                'data': None
            }
        )
