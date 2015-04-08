from contributions.views.api import ApiRequest
from contributions.models.project import Project
from contributions.utils.decorators import required_json_attributes
from contributions.exceptions import NotFoundException


class ProjectApi(ApiRequest):
    def get(self, id=None):
        if id is None:
            all_projects = Project.get_all()
            data = {
                "objects": all_projects,
                "num_results": len(all_projects),
                "page": 1
            }
        else:
            data = Project.get_by_id(int(id))
            if data is None:
                raise NotFoundException

        self.jsonify(data)

    @required_json_attributes('id', 'project_number')
    def post(self, id=None):
        data = self.request.json
        project = Project.insert(**data)
        self.jsonify(project, 201)

    @required_json_attributes('id')
    def put(self, id=None):
        # TODO
        self.abort(501)

    @required_json_attributes('id')
    def delete(self, id=None):
        # TODO
        self.abort(501)
