from contributions.views import Request


class Success(Request):
    def get(self):
        self.render("success.html", {"user": self.user, "url": self.login_url})
