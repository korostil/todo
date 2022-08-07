import click
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from api import router
from app.database import database
from app.error_handlers import exceptions_handler, validations_handler
from app.settings import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.settings = settings  # type: ignore
app.include_router(router, prefix='/api')

app.add_exception_handler(RequestValidationError, validations_handler)
app.add_exception_handler(HTTPException, exceptions_handler)


@app.on_event('startup')
async def startup() -> None:
    await database.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    await database.disconnect()


@click.group()
def cli() -> None:
    pass


@cli.command()
def runserver() -> None:
    reload = settings.debug
    application = 'main:app' if reload else app
    uvicorn.run(
        application,
        host=settings.app_host,
        port=settings.app_port,
        debug=settings.debug,
        reload=reload,
        log_level=settings.log_level,
        timeout_keep_alive=settings.timeout_keep_alive,
        access_log=False,
        loop='uvloop',
    )


if __name__ == '__main__':
    cli()
