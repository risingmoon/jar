from wsgiref.simple_server import make_server


class Application(object):

    def __call__(self, environ, start_response):
        response_body = 'Request method: %s' % environ['REQUEST_METHOD']
        status = '200 OK'
        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response_body)))
        ]
        start_response(status, response_headers)
        return [response_body]


if __name__ == '__main__':
    httpd = make_server('localhost', 8051, Application())
    httpd.handle_request()
