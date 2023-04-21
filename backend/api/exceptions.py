from fastapi import HTTPException, status

__all__ = (
    'BadRequest',
    'NotFound',
    'Forbidden',
    'NotFound',
    'UnprocessableEntity',
    'ServiceUnavailable',
)


class CustomHTTPException(HTTPException):
    status: int

    def __init__(self, message: str = ''):
        super().__init__(
            status_code=self.status, detail=message or self.__class__.__name__
        )


class BadRequest(CustomHTTPException):
    status = status.HTTP_400_BAD_REQUEST


class Forbidden(CustomHTTPException):
    status = status.HTTP_403_FORBIDDEN


class NotFound(CustomHTTPException):
    status = status.HTTP_404_NOT_FOUND


class UnprocessableEntity(CustomHTTPException):
    status = status.HTTP_422_UNPROCESSABLE_ENTITY


class ServiceUnavailable(CustomHTTPException):
    status = status.HTTP_503_SERVICE_UNAVAILABLE
