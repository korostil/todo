import funcy

from models import Goal
from services.database import create_one, delete_one, get_one, update_one

create_one_goal = funcy.partial(create_one, model=Goal)
delete_one_goal = funcy.partial(delete_one, model=Goal)
get_one_goal = funcy.partial(get_one, model=Goal)
update_one_goal = funcy.partial(update_one, model=Goal)
