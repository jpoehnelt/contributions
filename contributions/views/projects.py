from contributions.views import Request


class ProjectsPage(Request):
    def get(self, project_id=None):
        if id is not None:
            self.render('projects.html', {"project_id": project_id})
        else:
            self.render('projects.html')