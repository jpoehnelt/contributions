import webapp2
from urls import routes


app = webapp2.WSGIApplication(routes, debug=True)