from contributions.views.api import ApiRequest
from contributions.models.commit import Commit
from contributions.models.project import Project
from contributions.models.contributor import Contributor
from contributions.utils.decorators import required_json_attributes
from contributions.exceptions import NotFoundException, ReferentialIntegrityError
from google.appengine.ext import ndb
import datetime
import logging
import math


class CommitApi(ApiRequest):
    def get(self, id=None):
        """
        This method gets one or all commits and returns the commits as json.
        :param id:
        :return:
        """

        if self.get_cached_response() is not None:
            self.return_cached_response()
            return

        if id is None:
            if 'project_id' in self.request.GET and 'contributor_id' in self.request.GET:
                # get all commits for a specific project and contributor
                # e.g. /api/commit?project_id=123&contributor_id=123
                project_id = int(self.request.get('project_id'))
                contributor_id = int(self.request.get('contributor_id'))
                qry = Commit.query(Commit.project == ndb.Key(Project, project_id),
                                   Commit.contributor == ndb.Key(Contributor, contributor_id))

            elif 'project_id' in self.request.GET:
                # get all commits for a specific project e.g. /api/commit?project_id=123
                project_id = int(self.request.get('project_id'))
                qry = Commit.query(Commit.project == ndb.Key(Project, project_id))

            elif 'contributor_id' in self.request.GET:
                # get all commits by this contributor e.g. /api/commit?contributor_id=123
                contributor_id = int(self.request.get('contributor_id'))
                qry = Commit.query(Commit.contributor == ndb.Key(Contributor, contributor_id))
            else:
                qry = Commit.query()

            try:
                page_size = self.request.get('page_size', 500, False)
                num_results = qry.count()

                if page_size == 'all':
                    page = 1
                    commits = qry.fetch()
                    num_pages = 1
                else:
                    page_size = int(page_size)
                    page = int(self.request.get('page', 1, False))
                    offset = (page - 1) * page_size
                    commits = qry.fetch(limit=page_size, offset=offset)
                    num_pages = int(math.ceil((num_results + 0.00) / page_size))
                    logging.info('offset: %d, page: %d, page_size: %d, num_pages: %d, results: %d' %(offset, page, page_size, num_pages, len(commits)))

                logging.info(len(commits))
                data = {
                    "objects": commits,
                    "num_results": num_results,
                    "page": page,
                    "num_pages": num_pages
                }

            except Exception as e:
                logging.info(e)
                self.abort(500)
            else:
                self.jsonify(data, cache_time=60*30)


        else:
            data = Commit.get_by_id(id)
            if data is None:
                raise NotFoundException()
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
        if data['contributor'].get() is None:
            logging.info("!!!!!!!!===== There was no contributor info ======!!!!!!!!")
            raise ReferentialIntegrityError()

        data['project'] = ndb.Key(Project, data['project'])
        if data['project'].get() is None:
            logging.info("!!!!!!!!===== There was no project info ======!!!!!!!!")
            raise ReferentialIntegrityError()

        commit = Commit.insert(**data)
        self.jsonify(commit, 201)

    def put(self, id=None):
        """
        Updates an existing entity. Creates json response of updated entity.
        :param id:
        :return:
        """
        data = self.request.json

        # id needs to be passed either in json or in url variable
        if id is not None:
            data['id'] = id
        elif 'id' in data:
            pass
        else:
            self.jsonify('No instance identifier.', 400)
            return

        # TODO This needs testing and fix for timezone.
        data['date'] = datetime.datetime.strptime(data['date'][0:-1], "%Y-%m-%dT%H:%M:%S")

         # Get key from id
        data['contributor'] = ndb.Key(Contributor, data['contributor'])
        if data['contributor'].get() is None:
            raise ReferentialIntegrityError()

        data['project'] = ndb.Key(Project, data['project'])
        if data['project'].get() is None:
            raise ReferentialIntegrityError()

        # do the update
        commit = Commit.update(**data)

        return self.jsonify(commit)


    @required_json_attributes('id')
    def delete(self, id=None):
        """
        Deletes the entity.
        :param id:
        :return: None
        """
        # TODO
        self.abort(501)
