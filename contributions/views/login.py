from contributions.views import Request


class Success(Request):
    def get(self):
        self.render("success.html", {"user": self.user, "login_url": self.login_url})
