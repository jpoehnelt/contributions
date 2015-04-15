from contributions.views import Request


class ContactPage(Request):
    def get(self):
        self.render('contact.html')