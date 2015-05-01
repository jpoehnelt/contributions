from contributions.views import Request
from contributions.models.project import Project
from contributions.models.commit import Commit
from contributions.models.contributor import Contributor
import logging

class ProjectsPage(Request):

	def get(self, project_id=None):
		# put 0 in the url for this view to get this part to propogate all the commit_counts
		if project_id is not None:
			owner = ""
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
				else: # get the owner's account to pass to the template
					owner = Contributor.query().filter(Contributor.username == project.owner).fetch()
					if len(owner) > 1:
						raise Exception("More than one owner returned! " + str([o.username for o in owner]))
					elif len(owner) == 0:
						raise Exception("No owner was found! ")
					else:
						owner = owner[0]  # get rid of the list

			self.render('projects_single.html', {"project": project,
                                                 "owner": owner,
                                                 "user": self.user,
                                                 "login_url": self.login_url})

		else:
			qry = Project.query()
			projects = qry.fetch()
			self.render('projects_all.html', {"projects": projects,
                                              "user": self.user,
                                              "login_url": self.login_url})