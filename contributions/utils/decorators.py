from functools import wraps
from contributions.exceptions import MissingAttribute


def required_json_attributes(*attributes):
    """
    This method can be used to decorate request handler methods to check that all required json
    attributes were passed to the server. Raises an exception on first attribute not found.

    Example Usage:
    > @required_json_attributes('id', 'username', 'name', 'email')
    > def post(self, id=None):
    >    data = self.request.json
    >    project = Contributor.insert(**data)
    >    self.jsonify(project, 201)

    :param attributes:
    :return: None
    """
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