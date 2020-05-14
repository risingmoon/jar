from wsgiref.simple_server import make_server


class Request:

    def __init__(self, environ):
        prefix = 'HTTP_'
        self.headers = {}
        for key, value in environ.items():
            if key.startswith(prefix):
                self.headers[key[len(prefix)].lower()] = value


class Application:

    def __call__(self, environ, start_response):
        request = Request(environ)

        # response_body = 'Request method: %s' % environ['REQUEST_METHOD']
        response_body = b'Test'
        status = '200 OK'
        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response_body)))
        ]
        start_response(status, response_headers)
        return [response_body]


app = Application()
if __name__ == '__main__':
    httpd = make_server('localhost', 8000, Application())
    httpd.handle_request()