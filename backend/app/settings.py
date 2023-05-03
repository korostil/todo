from enum import Enum

from pydantic import BaseSettings, ValidationError


class Environment(str, Enum):
    LOCAL = 'local'
    TESTING = 'test'
    STAGING = 'stage'
    PRODUCTION = 'prod'


class Settings(BaseSettings):
    # Environment
    debug: bool = False
    environment: str = Environment.LOCAL
    timeout_keep_alive: int = 10

    # App
    app_name: str = 'todo'
    app_host: str = '0.0.0.0'
    app_port: int = 8000
    auth_token: str = 'secret_token'

    # Database
    db_host: str = 'db'
    db_port: int = 5432
    db_name: str = 'todo'
    db_user: str = 'todo'
    db_password: str = 'todo'

    # Logging
    log_level: str = 'info'

    # limits
    max_tasks_per_page = 50

    @property
    def database_url(self) -> str:
        user_creds = f'{self.db_user}:{self.db_password}'
        db_creds = f'{self.db_host}:{self.db_port}/{self.db_name}'
        if self.is_testing_environment:
            db_creds = f'{db_creds}_test'
        return f'postgresql+asyncpg://{user_creds}@{db_creds}'

    @property
    def is_testing_environment(self) -> bool:
        return self.environment == Environment.TESTING

    class Config:
        env_file = ".env"


try:
    settings = Settings()
except ValidationError:
    # TODO log error
    raise SystemExit(1)
