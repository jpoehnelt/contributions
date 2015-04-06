from contributions.settings import JINJA_ENVIRONMENT
import webapp2
from google.appengine.api import users


class Request(webapp2.RequestHandler):
    """
    Added functionality includes injecting user and shortcut for jinja rendering
    """
    def __init__(self, *args, **kwargs):
        # inject user in request
        self.user = users.get_current_user()

        # call parent class to initialize
        super(Request, self).__init__(*args, **kwargs)

    def render(self, template, context=None):
        """
        Helper function for rendering templates with jinja.

        :param template: path to .html
        :param context: dictionary of values to pass to jinja
        :return: a rendered template
        """
        if context is None:
            context = {}

        context['user'] = self.user

        self.response.write(JINJA_ENVIRONMENT.get_template(template).render(context))
