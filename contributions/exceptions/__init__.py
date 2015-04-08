from webapp2 import HTTPException
import json


class JSONHTTPException(HTTPException):
    def to_dict(self):
        return dict(error=self.error, code=self.code)


class NotFoundException(JSONHTTPException):
    def __init__(self):
        self.error = "Entity Not Found"
        self.code = 404


class DuplicateEntity(JSONHTTPException):
    def __init__(self):
        self.error = "Duplicate Entity"
        self.code = 409


class MissingAttribute(JSONHTTPException):
    def __init__(self):
        self.error = "Missing Attribute"
        self.code = 400