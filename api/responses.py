from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from funcy import is_seqcont

from utils import dumps

__all__ = ('APIResponse',)


class APIResponse(JSONResponse):
    media_type = 'application/json'

    def render(self, content: Any) -> Any:
        if content is None:
            return None

        if is_seqcont(content):
            data: list = list(content)
            content = {'status': 'ok', 'data': data, 'count': len(data)}
        else:
            content = {'status': 'ok', 'data': content}

        return dumps(jsonable_encoder(content)).encode('utf-8')
