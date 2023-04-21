from functools import partial

from ujson import dumps, loads

__all__ = ('dumps', 'loads')

dumps = partial(dumps, ensure_ascii=False)
