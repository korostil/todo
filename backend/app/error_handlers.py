from http import HTTPStatus

from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def validations_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return error_response(
        message=get_error_message(exc),
        status_code=HTTPStatus.BAD_REQUEST,
        code='bad_request',
    )


def get_error_message(exc: ValidationError) -> str:
    message: str = exc.errors()[0]['msg']
    field_name = exc.errors()[0]['loc'][-1]

    # If error raising in root validator, field_name == __root__.
    # Show only error message
    if field_name != '__root__':
        message = f'{field_name} {message}'

    return message


async def exceptions_handler(request: Request, exc: HTTPException) -> JSONResponse:
    status = HTTPStatus(exc.status_code)
    error_name = status.phrase.lower().replace(' ', '_')
    return error_response(
        message=exc.detail, status_code=exc.status_code, code=error_name
    )


def error_response(
    code: str = 'server_error', status_code: int = 500, message: str = ''
) -> JSONResponse:
    return JSONResponse(
        serialize_error_response(code, message), status_code=status_code
    )


def serialize_error_response(code: str, message: str) -> dict:
    return {'status': 'error', 'error': {'code': code, 'message': message}}
