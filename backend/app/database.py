import databases
from sqlalchemy.ext.declarative import declarative_base

from app.settings import settings

BaseDBModel = declarative_base()
if settings.is_testing_environment:
    database = databases.Database(settings.database_url, force_rollback=True)
else:
    database = databases.Database(settings.database_url)
