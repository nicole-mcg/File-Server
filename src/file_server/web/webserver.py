#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie

from file_server.web.endpoints.active_clients import ActiveClientsEndpoint
from file_server.web.endpoints.client_info import ClientInfoEndpoint

import webbrowser

import os

class RequestHandler(BaseHTTPRequestHandler):
    server = None
    endpoints = {}

    def _set_headers(self, code=200, content_type="text/html", expires=False):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.send_header('Set-Cookie', 'test=1234')

        if expires:
            self.send_header("Expires", "Mon, 01 Jan 1990 00:00:00 GMT")
        
        self.end_headers()

    def do_GET(self):
        cookie_data = self.headers.get('Cookie')

        if (cookie_data is not None):
            cookie = SimpleCookie()
            cookie.load(cookie_data)
        else:
            #We've got a new session
            pass

        try:

            endpoints = RequestHandler.endpoints
            path = self.path

            code = 200
            content_type = "text/html"
            expires = False

            if path.startswith("/api"):
                path = path[4:]

                index = path.find("/", 1)
                if index == -1:
                    endpoint = path
                else:
                    endpoint = path[:index]

                id = -1
                try: 
                    id = path[len(endpoint) + 1:]
                    id = int(id)
                except (ValueError, IndexError) as e:
                    pass

                #code = 403
                content_type = "application/json"
                contents = str.encode(endpoints[endpoint].handle_request(self, RequestHandler.server, id))

                expires = True

            else:

                if path.endswith(".js"):
                    content_type = "application/javascript"
                elif path.endswith(".css"):
                    content_type = "text/css"
                elif path.endswith(".jpg"):
                    content_type = "image/jpg"
                elif path.endswith(".gif"):
                    content_type = "image/gif"
                elif path.endswith(".png"):
                    content_type = "image/png"
                elif path.endswith(".svg"):
                    content_type = "image/svg+xml"
                else:
                    path = "/index.html"

                with open("." + path, "rb") as content_file:
                    contents = content_file.read()

            self._set_headers(code, content_type, expires)

            self.wfile.write(contents)

        except (IOError, KeyError) as e:
            print(e)
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(b"<html><body><h1>POST!</h1></body></html>")
        
def start_webserver(server):
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RequestHandler)

    os.chdir("../web")

    RequestHandler.server = server
    RequestHandler.endpoints = {
        "/activeclients": ActiveClientsEndpoint(),
        "/clientinfo": ClientInfoEndpoint(),
    }

    webbrowser.open('http://127.0.0.1:8080', new=2)
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    print("Starting webserver")

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()


#https://gist.github.com/bradmontgomery/2219997