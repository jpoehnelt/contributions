from contributions.models.commit import Commit, Project, Contributor
from contributions import app
from google.appengine.ext import testbed
import webtest
import unittest
import json

JSON_HEADERS = {"Content-Type": "application/json"}




class TestCommitApi(unittest.TestCase):
    def setUp(self):
        self.test_app = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(app_id='contributions-907')
        self.testbed.activate()
        self.testbed.init_all_stubs()

    def tearDown(self):
        self.testbed.deactivate()

    def create_contributor(self):
        data = {
            "id": 123123,
            "email": "email@something.com",
            "name": "Justin Poehnelt",
            "username": "justinwp",
            "avatar_url": "https://avatars.githubusercontent.com/u/3392975?v=3"
        }

        contributor = Contributor(**data)
        contributor.put()

        return contributor

    def create_project(self):
        data = {
            "id": 123123123,
            "owner": "user",
            "name": "some-repo1",
            "project_number": 1,
            "commit_count": 205
        }
        project = Project(**data)
        project.put()

        return project

    def test_get_all(self):
        contributor = self.create_contributor()
        project = self.create_project()

        data = {
            "id": "1231lkjdafd-Random-Hash-1231231",
            "project": project.key.id(),
            "contributor": contributor.key.id(),
            "date": "2015-01-23T16:05:50Z",
            "message": "bad commit message here",
            "changes": 5,
            "additions": 2,
            "deletions": 3,
        }

        response = self.test_app.post('/api/commit', params=json.dumps(data),
                                        headers=JSON_HEADERS, status=201)

        response = self.test_app.get('/api/commit')
        self.assertIsInstance(response.json['objects'], list)

        # test bad queries
        response = self.test_app.get('/api/commit?project_id=%d' % 1, status=200)
        self.assertEqual(len(json.loads(response.body)['objects']), 0)

        response = self.test_app.get('/api/commit?project_id=%d' % 1, status=200)
        self.assertEqual(len(json.loads(response.body)['objects']), 0)

        # test good queries
        response = self.test_app.get('/api/commit', status=200)
        self.assertEqual(len(json.loads(response.body)['objects']), 1)

        response = self.test_app.get('/api/commit?project_id=%d' % data['project'], status=200)
        self.assertEqual(len(json.loads(response.body)['objects']), 1)

        response = self.test_app.get('/api/commit?contributor=%d' % data['contributor'], status=200)
        self.assertEqual(len(json.loads(response.body)['objects']), 1)

        response = self.test_app.get(
            '/api/commit?project_id=%d&contributor_id=%d' % (data['project'], data['contributor']),
            status=200)
        self.assertEqual(len(json.loads(response.body)['objects']), 1)

    def test_get_single(self):
        contributor = self.create_contributor()
        project = self.create_project()

        data = {
            "id": "1231lkjdafd-Random-Hash-1231231",
            "project": project.key.id(),
            "contributor": contributor.key.id(),
            "date": "2015-01-23T16:05:50Z",
            "message": "bad commit message here",
            "changes": 5,
            "additions": 2,
            "deletions": 3,
        }

        response = self.test_app.post('/api/commit', params=json.dumps(data),
                                        headers=JSON_HEADERS, status=201)
        
        # This line breaks this test for some reason. Can't figure this out...
        self.test_app.get('/api/commit', status=200)
        # print'/api/commit/%s' % data['id']
        response = self.test_app.get('/api/commit/%s' % data['id'], status=200)
        self.assertEqual(json.loads(response.body)['id'], data['id'])

    def test_post(self):
        contributor = self.create_contributor()
        project = self.create_project()

        data = {
            "id": "1231lkjdafd-Random-Hash-1231231",
            "project": project.key.id(),
            "contributor": contributor.key.id(),
            "date": "2015-01-23T16:05:50Z",
            "message": "bad commit message here",
            "changes": 5,
            "additions": 2,
            "deletions": 3,
        }

        response = self.test_app.post('/api/commit', params=json.dumps(data),
                                      headers=JSON_HEADERS, status=201)

        # Test Duplicate Response
        response = self.test_app.post('/api/commit', params=json.dumps(data),
                                      headers=JSON_HEADERS, status=409)
        self.assertEqual(response.json['error'], 'Duplicate Entity')

        # Test Missing Attribute
        bad_data = {
            "id": "1231lkjdafd-Random-Hash-1231231",
        }
        response = self.test_app.post('/api/commit', params=json.dumps(bad_data),
                                      headers=JSON_HEADERS, status=400)