from contributions.views import Request
from contributions.models.project import Project


class ProjectApi(Request):
    def get(self):
        all_projects = Project.get_all()
        data = {
            "objects": all_projects,
            "num_results": len(all_projects),
            "page": 1
        }

        self.jsonify(data)

