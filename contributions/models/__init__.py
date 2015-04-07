from google.appengine.ext import ndb
from contributions.exceptions import DuplicateEntity


class CustomModel(ndb.Model):
    """
    Add a few more methods that are more compatible with a rest api.
    """

    @classmethod
    def get_all(cls):
        return cls.query().fetch()

    @classmethod
    def get_instance(cls, id):
        return cls.get_by_id(id)

    @classmethod
    @ndb.transactional(retries=1)
    def insert(cls, **kwargs):
        """
         This method does not allow overwriting entities and raises an exception if the entity
         already exists.
        """
        # Unique Key

        id = kwargs['id']

        key = ndb.Key(cls, id)

        # Get Entity with Key
        entity = key.get()

        # Check if Entity is None
        if entity is not None:
            raise DuplicateEntity()

        # Create Entity
        entity = cls(**kwargs)
        entity.key = key

        # Save to Datastore
        entity.put()
        return entity

    @classmethod
    @ndb.transactional(retries=1)
    def update(cls, **kwargs):
        pass
        #todo
