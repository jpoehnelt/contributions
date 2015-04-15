from contributions.views import Request


class AboutPage(Request):
    def get(self):
        self.render('about.html')
