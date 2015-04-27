from contributions.views import Request
from contributions.models.project import Project
from contributions.models.commit import Commit
import logging

class ProjectsPage(Request):
    def get(self, project_id=None):
        if id is not None:
        	# # testing putting a project in the db
        	# project = Project(id=29870404,
        	# 				  name='cs399_the_theatre',
        	# 				  owner='mkgilbert',
        	# 				  project_number=3)
        	# proj_key = project.put() # now in the database
        	# # now let's get the object we made
        	# project = proj_key.get()
        	logging.debug("The project id requested was " + str(project_id))
        	project = Project.get_by_id(project_id)
        	if project is None:
        		raise Exception("None Type Project was returned --> id was " + str(project_id))
        	else:
        		count = Commit.query().filter(project=project.key).count()

        	self.render('projects_single.html', {"project_id": project_id, "count": count})
        else:
        	qry = Project.query()
        	projects = qry.fetch()
        	self.render('projects_all.html', {"projects": projects})