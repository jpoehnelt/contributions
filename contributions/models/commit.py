from contributions.models import CustomModel
from contributions.models.project import Project
from contributions.models.contributor import Contributor
from google.appengine.ext import ndb


class Commit(CustomModel):
    project = ndb.KeyProperty(Project, required=True)
    contributor = ndb.KeyProperty(Contributor, required=True)

    date = ndb.DateTimeProperty()
    message = ndb.StringProperty()

    changes = ndb.IntegerProperty()
    additions = ndb.IntegerProperty()
    deletions = ndb.IntegerProperty()

    files_total = ndb.IntegerProperty()
    files_python = ndb.IntegerProperty()
    files_html = ndb.IntegerProperty()
    files_css = ndb.IntegerProperty()
    files_js = ndb.IntegerProperty()
    files_other = ndb.IntegerProperty()