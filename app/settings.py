from pydantic import BaseSettings, ValidationError


class Settings(BaseSettings):
    # Environment
    timeout_keep_alive: int = 10
    debug: bool = False

    # App
    app_name: str = 'todo'
    app_host: str = '0.0.0.0'
    app_port: int = 8000

    # Logging
    log_level: str = 'info'


try:
    settings = Settings()
except ValidationError:
    # TODO log error
    raise SystemExit(1)
