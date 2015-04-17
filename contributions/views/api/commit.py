from contributions.views.api import ApiRequest
from contributions.models.commit import Commit
from contributions.models.project import Project
from contributions.models.contributor import Contributor
from contributions.utils.decorators import required_json_attributes
from contributions.exceptions import NotFoundException
from google.appengine.ext import ndb
import datetime

class CommitApi(ApiRequest):
    def get(self, id=None):
        """
        This method gets one or all commits and returns the commits as json.
        :param id:
        :return:
        """

        # TODO Implement filtering. /api/commits?project=1231231

        if id is None:
            # get all of the commits to start with
            qry = Commit.query()

            if 'project_id' in self.request.GET:
                # get all commits for a specific project e.g. /api/commit?project_id=123
                project_id = self.request.get('project_id')
                qry = qry.filter(Commit.get_by_id(project_id))

            if 'contributor_id' in self.request.GET:
                # get all commits by this contributor e.g. /api/commit?contributor_id=123
                contrib_id = self.request.get('contributor_id')
                qry = qry.filter(Commit.get_by_id(contrib_id))

            commits = qry.fetch()
            data = {
                "objects": commits,
                "num_results": len(commits),
                "page": 1
            }

        else:
            data = Commit.get_by_id(id)
            if data is None:
                raise NotFoundException

        self.jsonify(data)

    @required_json_attributes('id', 'contributor', 'project')
    def post(self, id=None):
        """
        Inserts a new entity into the data store.
        :param id:
        :return:
        """
        data = self.request.json

        # TODO This needs testing and fix for timezone.
        data['date'] = datetime.datetime.strptime(data['date'][0:-1], "%Y-%m-%dT%H:%M:%S")

        # Get key from id
        data['contributor'] = ndb.Key(Contributor, data['contributor'])
        data['project'] = ndb.Key(Project, data['project'])

        # TODO handle exceptions from google ndb insert method

        commit = Commit.insert(**data)

        self.jsonify(commit, 201)

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
        # TODO
        self.abort(501)
