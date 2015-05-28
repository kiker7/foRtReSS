from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

start = """
<!DOCTYPE html>
<html>
<body>
   <a href="index.html">Home</a>
   <a href="nowy.html">Nowy</a>
   PATH_INFO: %s
</body>
</html>"""

def load_mainpage():
    return start % ("Dupa")

def application(environ, start_response):
    path = environ.get('PATH_INFO')
    if path == '/':
        response_body = load_mainpage()
    elif path == '/nowy.html':
        response_body = start % ("Siema")
    else:
        response_body = start % (path)
    
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'),('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]

if __name__ == '__main__':
    httpd = make_server('localhost', 8000, application)
    httpd.serve_forever()