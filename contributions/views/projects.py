from contributions.views import Request


class ProjectsPage(Request):
    def get(self):
        self.render('projects.html')