from contributions.views import Request
from contributions.exceptions import JSONHTTPException
from contributions.utils.serializers import JSONEncoder


class ApiRequest(Request):
    def handle_exception(self, exception, debug):
        print exception
        if isinstance(exception, JSONHTTPException):
            self.jsonify(exception.to_dict(), exception.code)
        else:
            self.response.set_status(500)

    def jsonify(self, data, code=200):
        self.response.set_status(code)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(JSONEncoder().encode(data))