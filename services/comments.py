import funcy

from models import Comment
from services.database import create_one, delete_one, get_one, update_one

create_one_comment = funcy.partial(create_one, model=Comment)
delete_one_comment = funcy.partial(delete_one, model=Comment)
get_one_comment = funcy.partial(get_one, model=Comment)
update_one_comment = funcy.partial(update_one, model=Comment)
