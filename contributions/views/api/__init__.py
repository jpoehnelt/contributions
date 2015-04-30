from contributions.views import Request
from contributions.exceptions import JSONHTTPException
from contributions.utils.serializers import JSONEncoder
import logging
from google.appengine.api import memcache


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

    def jsonify(self, data, code=200, cache_time=0):
        """
        This is a shortcut method for returning a json response.
        :param data: JSON String
        :param code: HTTP Status Code
        :return: None
        """
        # TODO error handling if data is not JSON string... check type, if not string JSON Encode?

        self.response.set_status(code)
        self.response.headers['Content-Type'] = 'application/json'
        if not isinstance(data, str):
            data = JSONEncoder().encode(data)
        self.response.out.write(data)
        if cache_time > 0:
            self.set_cached_response(data, cache_time)

    def get_cached_response(self):
        key = self.request.method + self.request.url
        return memcache.get(key)

    def set_cached_response(self, data, time=60*5):
        key = self.request.method + self.request.url
        try:
            memcache.set(key, data, time=time)
        except Exception as e:
            logging.info(e)

    def return_cached_response(self):
        data = self.get_cached_response()
        logging.info(type(data))

        self.jsonify(data)