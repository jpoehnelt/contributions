from contributions.views.api import ApiRequest
from contributions.models.project import Project
from contributions.utils.decorators import required_json_attributes
from contributions.exceptions import NotFoundException
import logging

class ProjectApi(ApiRequest):
    def get(self, id=None):
        logging.info('Handling Get')

        """
        This method gets one or all projects and returns the projects as json.
        :param id:
        :return:
        """

        # TODO Implement filtering. /api/project?project_number=2

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

    @required_json_attributes('id', 'name', 'owner', 'project_number')
    def post(self, id=None):
        """
        Inserts a new entity into the data store.
        :param id:
        :return:
        """
        logging.info('Handling Post')
        logging.info(id)
        data = self.request.json
        project = Project.insert(**data)
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
        # TODO
        self.abort(501)
