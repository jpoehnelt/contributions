from contributions import app
from google.appengine.ext import testbed
import unittest
import webtest
import json

JSON_HEADERS = {"Content-Type": "application/json"}


class TestProjectApi(unittest.TestCase):
    def setUp(self):
        self.test_app = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(app_id='contributions-907')
        self.testbed.activate()
        self.testbed.init_all_stubs()

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_all(self):
        response = self.test_app.get('/api/project')
        self.assertIsInstance(response.json['objects'], list)

    def test_get_single(self):
        pass

    def test_post(self):
        data = {
            "id": "user/name",
            "project_number": 1,
            "commit_count": 205
        }

        response = self.test_app.post('/api/project', params=json.dumps(data),
                                      headers=JSON_HEADERS, status=201)

        self.assertDictEqual(data, response.json)

        # Test Duplicate Response
        response = self.test_app.post('/api/project', params=json.dumps(data),
                                      headers=JSON_HEADERS, status=409)
        self.assertEqual(response.json['error'], 'Duplicate Entity')

        # Test Missing Attribute
        bad_data = {
            "id": "user/name",
        }
        response = self.test_app.post('/api/project', params=json.dumps(bad_data),
                                      headers=JSON_HEADERS, status=400)