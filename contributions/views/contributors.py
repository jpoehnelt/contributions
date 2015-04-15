from contributions.views import Request


class ContributorsPage(Request):
    def get(self, contributor_id=None):
        if id is not None:
            self.render('contributors_single.html', {"contributor_id": contributor_id})
        else:
            self.render('contributors_all.html')