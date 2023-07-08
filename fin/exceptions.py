from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def valid_except_handler(
        request: Request,
        exc: RequestValidationError
) -> JSONResponse:
    """Request valid handler"""
    # ToDo implement

    return JSONResponse(status_code=exc.status_code, content=f'{exc.detail}')


async def http_except_handler(
        request: Request,
        exc: RequestValidationError
) -> JSONResponse:
    """HTTP exception handler"""
    # ToDo implement
    return JSONResponse(status_code=exc.status_code, content=f'{exc.detail}')


class NoMatchError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=409, detail="No match fingerprint", headers={})
