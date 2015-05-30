#!/usr/bin/env python

# Imports
from wsgiref.simple_server import make_server

# Global variables
SERVER_IP_ADDRESS = '127.0.0.1'
SERVER_PORT = 8000
RESOURCES_LOCATION = 'resources'
EXTENSIONS = {
    '.css': 'text/css',
    '.gif': 'image/gif',
    '.htm': 'text/html',
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.jpeg': 'image/jpeg',
    '.jpg': 'image/jpeg',
    '.png': 'image/png',
    '.ico': 'image/x-icon',
    '.text': 'text/plain',
    '.txt': 'text/plain',
}

# Application object
class Application:
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO')
        
        file = path[path.rfind('/'):]
        extension = file[file.rfind('.'):]
        if '.' not in extension:
            if path == '/':
                content_type = 'text/html'
            else:
                content_type = 'text/plain'
        elif extension in EXTENSIONS:
            content_type = EXTENSIONS[extension]
        response_headers = [('Content-type', content_type)]
        
        response_body = self.open_file(path)
        
        status = '200 OK'
        start_response(status, response_headers)
        return response_body
    
    def open_file(self, path):
        path = RESOURCES_LOCATION + path
        if path == "resources/":
            path += 'mainpage.html'
        file = open(path, "rb")
        content = file.read()
        file.close()
        return content
    
if __name__ == '__main__':
    application = Application()
    httpd = make_server(SERVER_IP_ADDRESS, SERVER_PORT, application)
    httpd.serve_forever()
