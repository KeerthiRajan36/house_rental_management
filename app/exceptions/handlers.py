from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import *


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AuthenticationException)
    async def authentication_exception_handler(
        request: Request,
        exc: AuthenticationException
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": exc.message
            }
        )

    @app.exception_handler(AuthorizationException)
    async def authorization_exception_handler(
        request: Request,
        exc: AuthorizationException
    ):
        return JSONResponse(
            status_code=403,
            content={
                "success": False,
                "message": exc.message
            }
        )

    @app.exception_handler(ResourceNotFoundException)
    async def not_found_exception_handler(
        request: Request,
        exc: ResourceNotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": exc.message
            }
        )

    @app.exception_handler(DuplicateRecordException)
    async def duplicate_exception_handler(
        request: Request,
        exc: DuplicateRecordException
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": exc.message
            }
        )

    @app.exception_handler(ValidationException)
    async def validation_exception_handler(
        request: Request,
        exc: ValidationException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.message
            }
        )

    @app.exception_handler(HouseOccupiedException)
    async def occupied_exception_handler(
        request: Request,
        exc: HouseOccupiedException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.message
            }
        )

    @app.exception_handler(TenantAlreadyAssignedException)
    async def tenant_assigned_handler(
        request: Request,
        exc: TenantAlreadyAssignedException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.message
            }
        )

    @app.exception_handler(DuplicatePaymentException)
    async def payment_exception_handler(
        request: Request,
        exc: DuplicatePaymentException
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": exc.message
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error"
            }
        )