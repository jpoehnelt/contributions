from contributions.models import CustomModel
from google.appengine.ext import ndb


class Contributor(CustomModel):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    avatar_url = ndb.StringProperty()