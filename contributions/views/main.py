from contributions.views import Request


class MainPage(Request):
    def get(self):
        self.render('index.html')