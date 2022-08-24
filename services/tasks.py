import funcy

from models import Task
from services.database import create_one, delete_one, get_one, update_one

create_one_task = funcy.partial(create_one, model=Task)
delete_one_task = funcy.partial(delete_one, model=Task)
get_one_task = funcy.partial(get_one, model=Task)
update_one_task = funcy.partial(update_one, model=Task)
