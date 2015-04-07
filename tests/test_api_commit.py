from contributions import app
from google.appengine.ext import testbed
import unittest
import webtest
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

    def test_get_all(self):
        response = self.test_app.get('/api/commit')
        self.assertIsInstance(response.json['objects'], list)

    def test_get_single(self):
        pass

    def test_post(self):
        data = {
            "id": "1231lkjdafd-Random-Hash-1231231",
            "repo_id": "justinwp/reponame",
            "contributor_id": 'justinwp',
            "date": "2015-01-23T16:05:50Z",
            "message": "bad commit message here",
            "changes": 5,
            "additions": 2,
            "deletions": 3,
            "python_changes": 2,
            "python_additions": 1,
            "python_deletions": 1,
            "js_changes": 1,
            "js_additions": 0,
            "js_deletions": 1,
            "html_changes": 1,
            "html_additions": 1,
            "html_deletions": 0,
            "other_changes": 1,
            "other_additions": 1,
            "other_deletions": 0,
        }

        response = self.test_app.post('/api/commit', params=json.dumps(data),
                                      headers=JSON_HEADERS, status=201)

        self.assertDictEqual(data, response.json)

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