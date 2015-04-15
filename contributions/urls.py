from views.main import MainPage
from views.about import AboutPage
from views.api.project import ProjectApi
from views.api.commit import CommitApi
from views.api.contributor import ContributorApi


routes = [
    ('/', MainPage),
    ('/about', AboutPage),
    ('/api/project', ProjectApi),
    ('/api/project/(\d+)', ProjectApi),
    ('/api/commit', CommitApi),
    ('/api/commit/(\s+)', CommitApi),
    ('/api/contributor', ContributorApi),
    ('/api/contributor/(\d+)', ContributorApi),
]