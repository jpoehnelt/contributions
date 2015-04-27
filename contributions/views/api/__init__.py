from contributions.views import Request
from contributions.exceptions import JSONHTTPException
from contributions.utils.serializers import JSONEncoder


class ApiRequest(Request):
    def handle_exception(self, exception, debug):
        """
        This method handles any exceptions that are raised during the processing of requests and
        the accompanying response. It modifies the Response object.

        :param exception:
        :param debug:
        :return: None
        """
        if isinstance(exception, JSONHTTPException):
            self.jsonify(exception.to_dict(), exception.code)
        else:
            self.jsonify(exception.__dict__, 500)

    def jsonify(self, data, code=200):
        """
        This is a shortcut method for returning a json response.
        :param data: JSON String
        :param code: HTTP Status Code
        :return: None
        """
        # TODO error handling if data is not JSON string... check type, if not string JSON Encode?
        self.response.set_status(code)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(JSONEncoder().encode(data))