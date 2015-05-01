from contributions.views import Request
from contributions.models.commit import Commit
from contributions.models.contributor import Contributor 


class ContributorsPage(Request):

    def get(self, contrib_id=None):
        qry = Contributor.query()
        if contrib_id is not None:
            if int(contrib_id) == 0:
                contribs = qry.filter(Contributor.avatar_url == None).fetch()
                for contrib in contribs:
                    contrib.avatar_url = "/static/images/default_contrib_thumb.png"
                    contrib.put()
            else:
                # get the contributor
                contrib = Contributor.get_by_id(int(contrib_id))
                if contrib is None:
                    raise Exception("None Type Project was returned --> id was " + str(contrib_id))
                else:
                    # get all their commits
                    qry = Commit.query().filter(Commit.contributor == contrib.key)
                    commits = qry.order(Commit.project).fetch()
            self.render('contributors_single.html', {"contrib": contrib, "commits": commits,
                                                     "user": self.user, "login_url": self.login_url})
        else:
            contribs = qry.fetch()
            self.render('contributors_all.html', {"contribs": contribs,
                                                  "user": self.user,
                                                  "login_url": self.login_url} )