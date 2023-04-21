import funcy

from models import Project
from services.database import create_one, delete_one, get_one, update_one

create_one_project = funcy.partial(create_one, model=Project)
delete_one_project = funcy.partial(delete_one, model=Project)
get_one_project = funcy.partial(get_one, model=Project)
update_one_project = funcy.partial(update_one, model=Project)
