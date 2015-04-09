from google.appengine.ext import ndb
from contributions.exceptions import DuplicateEntity


class CustomModel(ndb.Model):
    """
    Add a few more methods that are more compatible with a rest api and enforcement of entity
    integrity.
    """

    @classmethod
    def get_all(cls):
        """
        Returns all entities of type cls.
        :return:
        """
        return cls.query().fetch()

    @classmethod
    @ndb.transactional(retries=1)
    def insert(cls, **kwargs):
        """
         This method works within an atomic transaction does not allow overwriting entities.
         It raises an exception if the entity already exists. Google ndb would simply overwrite the
         existing entity otherwise.
         :return: entity
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
        """
        Checks if an entity exists and if it does, it updates and returns the entity. If entity
        does not exist, raise an exception.
        :param kwargs:
        :return: entity
        """
        pass
        #todo
