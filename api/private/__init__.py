from fastapi import APIRouter, Depends

from .auth import validate_token
from .projects import router as projects_router
from .tasks import router as tasks_router

private_router = APIRouter(dependencies=[Depends(validate_token)])
private_router.include_router(projects_router)
private_router.include_router(tasks_router)
