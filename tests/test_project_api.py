from contributions import app
from google.appengine.ext import testbed
import unittest
import webtest


class TestProjectApi(unittest.TestCase):
    def setUp(self):
        self.test_app = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(app_id='contributions-907')
        self.testbed.activate()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_get(self):
        print "tests_get"
        pass