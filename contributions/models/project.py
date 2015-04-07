from google.appengine.ext import ndb


class Project(ndb.Model):
    """
    Model for representing a github project.
    """
    owner = ndb.StringProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)
    project_no = ndb.IntegerProperty(indexed=True)

    @classmethod
    def get_all(cls):
        return cls.query().fetch()

    @classmethod
    def get_instance(cls, key):
        return cls.get_by_id(key)