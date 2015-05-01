from contributions.settings import JINJA_ENVIRONMENT
import webapp2
from google.appengine.api import users
from contributions.utils.serializers import JSONEncoder
import json


class Request(webapp2.RequestHandler):
    """
    Added functionality includes injecting user and shortcut for jinja rendering
    """
    def __init__(self, *args, **kwargs):
        # inject user in request
        self.login_url = "/my_page"
        self.user = users.get_current_user()
        if self.user:
            self.login_url = users.create_logout_url('/')
        else:
            self.login_url = users.create_login_url('/success')

        # call parent class to initialize
        super(Request, self).__init__(*args, **kwargs)

        if 'Content-Type' in self.request.headers and \
            self.request.headers['Content-Type'] == 'application/json':
            self.request.json = json.loads(self.request.body)

    def render(self, template, context=None):
        """
        Helper function for rendering templates with jinja.

        :param template: path to .html
        :param context: dictionary of values to pass to jinja
        :return: a rendered template
        """
        if context is None:
            context = {}

        if self.user:
            context['user'] = self.user

        self.response.write(JINJA_ENVIRONMENT.get_template(template).render(context))
