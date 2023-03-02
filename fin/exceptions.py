from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def valid_except_handler(
        request: Request,
        exc: RequestValidationError
) -> JSONResponse:
    """Request valid handler"""
    # ToDo implement
    return JSONResponse(status_code=400, content='')


async def http_except_handler(
        request: Request,
        exc: RequestValidationError
) -> JSONResponse:
    """HTTP exception handler"""
    # ToDo implement
    return JSONResponse(status_code=400, content='')
