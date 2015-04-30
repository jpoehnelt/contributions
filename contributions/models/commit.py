from contributions.models import CustomModel
from contributions.models.project import Project
from contributions.models.contributor import Contributor
from google.appengine.ext import ndb


class File(ndb.Model):
    filename = ndb.StringProperty(required=True)
    status = ndb.StringProperty()
    additions = ndb.IntegerProperty()
    deletions = ndb.IntegerProperty()
    changes = ndb.IntegerProperty()


class Commit(CustomModel):
    project = ndb.KeyProperty(Project, required=True)
    contributor = ndb.KeyProperty(Contributor, required=True)

    date = ndb.DateTimeProperty()
    message = ndb.StringProperty()

    changes = ndb.IntegerProperty()
    additions = ndb.IntegerProperty()
    deletions = ndb.IntegerProperty()

    files = ndb.StructuredProperty(File, repeated=True)