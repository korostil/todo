from fastapi import APIRouter

from .private import private_router
from .responses import APIResponse

router = APIRouter(default_response_class=APIResponse)

router.include_router(private_router, prefix='/private/v1')
