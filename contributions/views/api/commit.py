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
        if id is None:
            all_commits = Commit.get_all()
            data = {
                "objects": all_commits,
                "num_results": len(all_commits),
                "page": 1
            }
        else:
            data = Project.get_by_id(id)
            if data is None:
                raise NotFoundException

        self.jsonify(data)

    @required_json_attributes('id', 'contributor', 'project')
    def post(self, id=None):
        data = self.request.json

        # TODO This needs testing and fix for timezone.
        data['date'] = datetime.datetime.strptime(data['date'][0:-1], "%Y-%m-%dT%H:%M:%S")

        # Get key from id
        data['contributor'] = ndb.Key(Contributor, data['contributor'])
        data['project'] = ndb.Key(Project, data['project'])

        # if data['contributor'] is None or data['project'] is None:
        #     # todo error handling
        #     pass

        commit = Commit.insert(**data)

        print commit
        self.jsonify(commit, 201)

    @required_json_attributes('id')
    def put(self, id=None):
        # TODO
        self.abort(501)

    @required_json_attributes('id')
    def delete(self, id=None):
        # TODO
        self.abort(501)
