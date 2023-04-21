from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.exceptions import Forbidden
from app.settings import settings


def validate_token(
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> None:
    if not settings.auth_token:
        return

    is_scheme_bearer = authorization.scheme == 'Bearer'
    is_token_valid = authorization.credentials == settings.auth_token

    if not is_scheme_bearer or not is_token_valid:
        raise Forbidden('Invalid token')
