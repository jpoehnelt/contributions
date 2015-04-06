import os
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def render_template(template, context=None):
    """
    Helper function for rendering templates with jinja.

    :param template: path to .html
    :param context: dictionary of values to pass to jinja
    :return: a rendered template
    """
    if context is None:
        context = {}
    return JINJA_ENVIRONMENT.get_template(template).render(context)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(render_template('templates/index.html'))

app = webapp2.WSGIApplication([
                                  ('/', MainPage),
                              ], debug=True)