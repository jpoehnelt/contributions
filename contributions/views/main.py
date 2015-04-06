from contributions.views import render_template
import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(render_template('index.html'))