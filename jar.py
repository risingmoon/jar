from collections import OrderedDict
from wsgiref.simple_server import make_server


def parse_accept(value):
    mapping = {}
    if value:
        items = value.split(',')
        for item in items:
            if ';' in item:
                key, q = item.split(';')
                mapping[key] = float(q.split('=')[1])
            else:
                mapping[item] = 1.0
    return mapping


class Accept:

    def __init__(self, environ):
        self.language = parse_accept(environ.pop('HTTP_ACCEPT_LANGUAGE', None))
        self.encoding = parse_accept(environ.pop('HTTP_ACCEPT_ENCODING', None))
        self.mime_type = parse_accept(environ.pop('HTTP_ACCEPT', None))
        self.charset = parse_accept(environ.pop('HTTP_ACCEPT_CHARSET', None))


class Request:

    def __init__(self, environ):
        prefix = 'HTTP_'
        self.headers = {}
        keys = [k for k in environ.keys() if k.startswith(prefix)]
        for key in keys:
            value = environ.pop(key)
            self.headers[key[len(prefix)].lower()] = value
        self.accept = Accept(self.headers)

    @property
    def host(self):
        return self.headers['HTTP_HOST']

    @property
    def user_agent(self):
        return self.headers['HTTP_USER_AGENT']


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
    httpd.serve_forever()

