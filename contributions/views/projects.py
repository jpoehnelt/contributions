from contributions.views import Request
from contributions.models.project import Project
from contributions.models.commit import Commit
import logging

class ProjectsPage(Request):

    def get(self, project_id=None):	
    	# put 0 in the url for this view to get this part to propogate all the commit_counts
       	if project_id is not None:
       		# this will query all commits for each project and put commit counts in db
        	if int(project_id) == 0:
        		qry = Project.query()
	    		projects = qry.fetch()
	    		for project in projects:
	    			count = Commit.query().filter(Commit.project == project.key).count()
	    			project.commit_count = count
	    			project.put()

	    	else:  # specific project is selected
        		project = Project.get_by_id(int(project_id))

	        	if project is None:
	        		raise Exception("None Type Project was returned --> id was " + str(project_id))

	        self.render('projects_single.html', {"project": project, "count": count})
        else:
        	qry = Project.query()
        	projects = qry.fetch(30)
        	self.render('projects_all.html', {"projects": projects})