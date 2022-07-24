import click
import uvicorn
from fastapi import FastAPI

from api import router
from app.settings import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(router, prefix='/api')


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
