from fastapi import APIRouter, Depends

from .auth import validate_token
from .comments import router as comments_router
from .goals import router as goals_router
from .projects import router as projects_router
from .tags import router as tags_router
from .tasks import router as tasks_router

private_router = APIRouter(dependencies=[Depends(validate_token)])
private_router.include_router(projects_router)
private_router.include_router(tasks_router)
private_router.include_router(tags_router)
private_router.include_router(comments_router)
private_router.include_router(goals_router)
