from functools import wraps
from contributions.exceptions import MissingAttribute


def required_json_attributes(*attributes):
    def wrapper(fn):
        @wraps(fn)
        def decorated_method(*args, **kwargs):
            self = args[0]
            for attr in attributes:
                if attr not in self.request.json:
                    raise MissingAttribute()
            return fn(*args, **kwargs)
        return decorated_method
    return wrapper