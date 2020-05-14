from collections import OrderedDict
from wsgiref.simple_server import make_server


class Request:

    def __init__(self, environ):
        prefix = 'HTTP_'
        self.headers = {}
        for key, value in environ.items():
            if key.startswith(prefix):
                self.headers[key[len(prefix)].lower()] = value


class Headers(OrderedDict):

    def __iter__(self):
        for key in super().__iter__():
            yield key, self[key]


class Response:

    def __init__(self, body=b'', status_code=200, content_type='text/plain'):
        self.status_code = status_code

        self.headers = Headers()
        self.body = body
        self.content_type = content_type

    @property
    def body(self, ):
        return self.content

    @body.setter
    def body(self, value):
        self.content = value
        self.headers['Content-Length'] = str(len(self.content))

    @property
    def content_type(self):
        return self.headers['Content-Type']

    @content_type.setter
    def content_type(self, value):
        self.headers['Content-Type'] = str(value)


class Application:

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response(b'Test')
        status = '200 OK'
        start_response(status, list(response.headers))
        return [response.body]


app = Application()
if __name__ == '__main__':
    httpd = make_server('localhost', 8000, Application())
    httpd.handle_request()

