import funcy

from models import Tag
from services.database import create_one, delete_one, get_one, update_one

create_one_tag = funcy.partial(create_one, model=Tag)
delete_one_tag = funcy.partial(delete_one, model=Tag)
get_one_tag = funcy.partial(get_one, model=Tag)
update_one_tag = funcy.partial(update_one, model=Tag)
