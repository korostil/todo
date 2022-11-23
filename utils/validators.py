from functools import partial

from pydantic import validator

reusable_validator = partial(validator, allow_reuse=True)
