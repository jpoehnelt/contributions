from contributions.models import CustomModel
from google.appengine.ext import ndb


class Project(CustomModel):
    """
    Model for representing a github project.
    """
    project_number = ndb.IntegerProperty(indexed=True, required=True)
    commit_count = ndb.IntegerProperty()