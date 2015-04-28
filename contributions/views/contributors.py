from contributions.views import Request
from contributions.models.commit import Commit
from contributions.models.contributor import Contributor 


class ContributorsPage(Request):

	def get(self, contrib_id=None):
		qry = Contributor.query()
		if contrib_id is not None:
			# get the contributor
			contrib = Contributor.get_by_id(int(contrib_id))
			if contrib is None:
				raise Exception("None Type Project was returned --> id was " + str(contrib_id))
			else:
				# get all their commits
				qry = Commit.query().filter(Commit.contributor == contrib.key)
				commits = qry.order(Commit.project).fetch()

			self.render('contributors_single.html', {"contrib": contrib, "commits": commits} )
		else:
			contribs = qry.fetch()
			self.render('contributors_all.html', {"contribs": contribs} )