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
        data = self.request.json
        project = Contributor.insert(**data)
        print project
        self.jsonify(project, 201)

    @required_json_attributes('id')
    def put(self, id=None):
        # TODO
        self.abort(501)

    @required_json_attributes('id')
    def delete(self, id=None):
        # TODO
        self.abort(501)
