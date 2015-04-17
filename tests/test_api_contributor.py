from contributions import app
from google.appengine.ext import testbed
import unittest
import webtest
import json

JSON_HEADERS = {"Content-Type": "application/json"}


class TestContributorApi(unittest.TestCase):
    def setUp(self):
        self.test_app = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(app_id='contributions-907')
        self.testbed.activate()
        self.testbed.init_all_stubs()

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_all(self):
        response = self.test_app.get('/api/contributor')
        self.assertIsInstance(response.json['objects'], list)

    def test_get_single(self):
        data = {
            "id": 123123,
            "email": "email@something.com",
            "name": "Justin Poehnelt",
            "username": "justinwp",
            "avatar_url": "https://avatars.githubusercontent.com/u/3392975?v=3"
        }

        response = self.test_app.post('/api/contributor', params=json.dumps(data),
                                      headers=JSON_HEADERS, status=201)

        #print response.json
        response = self.test_app.get('/api/contributor/%d'% data['id'], status=200)
        #print response

    def test_post(self):
        data = {
            "id": 123123,
            "email": "email@something.com",
            "name": "Justin Poehnelt",
            "username": "justinwp",
            "avatar_url": "https://avatars.githubusercontent.com/u/3392975?v=3"
        }

        response = self.test_app.post('/api/contributor', params=json.dumps(data),
                                      headers=JSON_HEADERS, status=201)
        print response.json
        self.assertDictEqual(data, response.json)

        # Test Duplicate Response
        response = self.test_app.post('/api/contributor', params=json.dumps(data),
                                      headers=JSON_HEADERS, status=409)
        self.assertEqual(response.json['error'], 'Duplicate Entity')

        # Test Missing Attribute
        bad_data = {
            "email": "email@something.com"
        }
        response = self.test_app.post('/api/contributor', params=json.dumps(bad_data),
                                      headers=JSON_HEADERS, status=400)