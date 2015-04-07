from views.main import MainPage
from views.api.project import ProjectApi


routes = [
    ('/', MainPage),
    ('/api/project', ProjectApi),
    ('/api/project/(\d+)', ProjectApi),
]