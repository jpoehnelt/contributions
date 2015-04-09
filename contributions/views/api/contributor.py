from contributions.views.api import ApiRequest
from contributions.models.contributor import Contributor
from contributions.utils.decorators import required_json_attributes
from contributions.exceptions import NotFoundException


class ContributorApi(ApiRequest):
    def get(self, id=None):
        if id is None:
            all_contributors = Contributor.get_all()
            data = {
                "objects": all_contributors,
                "num_results": len(all_contributors),
                "page": 1
            }
        else:
            data = Contributor.get_by_id(int(id))
            if data is None:
                raise NotFoundException
        self.jsonify(data)

    @required_json_attributes('id', 'username', 'name', 'email')
    def post(self, id=None):
        """
        Inserts a new entity into the data store.
        :param id:
        :return:
        """
        data = self.request.json
        project = Contributor.insert(**data)
        self.jsonify(project, 201)

    @required_json_attributes('id')
    def put(self, id=None):
        """
        Updates an existing entity. Creates json response of updated entity.
        :param id:
        :return:
        """
        # TODO Be careful since this is different than sql and will create a new entity if none exists.
        # Uses custom update method in custom model.
        self.abort(501)

    @required_json_attributes('id')
    def delete(self, id=None):
        """
        Deletes the entity.
        :param id:
        :return: None
        """
        #TODO
        # self.abort(501)
