from contributions.models import CustomModel
from google.appengine.ext import ndb


class Project(CustomModel):
    """
    Model for representing a github project.
    """
    owner = ndb.StringProperty(indexed=True, required=True)
    name = ndb.StringProperty(indexed=True, required=True)
    project_number = ndb.IntegerProperty(indexed=True, required=True)
    commit_count = ndb.IntegerProperty()