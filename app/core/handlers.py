from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    LeadNotFoundError,
    PropertyConflictError,
    PermissionDeniedError,
    UsernameAlreadyExistsError,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(LeadNotFoundError)
    async def lead_not_found_handler(request: Request, exc: LeadNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "error": str(exc)
            }
        )

    @app.exception_handler(PropertyConflictError)
    async def property_conflict_handler(request: Request, exc: PropertyConflictError):
        return JSONResponse(
            status_code=409,
            content={
                "error": str(exc)
            }
        )

    @app.exception_handler(PermissionDeniedError)
    async def permission_denied_handler(request: Request, exc: PermissionDeniedError):
        return JSONResponse(
            status_code=403,
            content={
                "error": str(exc)
            }
        )

    @app.exception_handler(UsernameAlreadyExistsError)
    async def username_exists_handler(
        request: Request,
        exc: UsernameAlreadyExistsError
    ):
        return JSONResponse(
            status_code=409,
            content={
                "error": str(exc)
            }
        )