from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie

from file_server.web.account import Account
from file_server.web.endpoints.active_clients import ActiveClientsEndpoint
from file_server.web.endpoints.client_info import ClientInfoEndpoint
from file_server.web.endpoints.login import LoginEndpoint
from file_server.web.endpoints.signup import SignupEndpoint

import webbrowser

import os

import json

class RequestHandler(BaseHTTPRequestHandler):
    server = None

    def _set_headers(self, account, code=200, content_type="text/html", expires=False):
        cookie_data = self.headers.get('Cookie')
        self.send_response(code)
        self.send_header('Content-type', content_type)

        if account is not None:
            self.send_header('Set-Cookie', 'session=' + account.session)

        if expires:
            self.send_header("Expires", "Mon, 01 Jan 1990 00:00:00 GMT")
        
        self.end_headers()

    def do_GET(self):
        

        account = None
        if (cookie_data is not None):
            cookie = SimpleCookie()
            cookie.load(cookie_data)

            if "session" in cookie:
                try:
                    account = Account.sessions[cookie["session"]]
                    print("account=" + account.name)
                except KeyError:
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
                elif path != "/login" and account is None:
                    print("redirecting to login")
                    print(path)
                    self.send_response(302)
                    self.send_header('Location','/login')
                    self.end_headers()
                    return
                else:
                    path = "/index.html"

                with open("." + path, "rb") as content_file:
                    contents = content_file.read()

            self._set_headers(account, code, content_type, expires)

            self.wfile.write(contents)

        except (IOError, KeyError) as e:
            print(e)
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_HEAD(self):
        self._set_headers(None)
        
    def do_POST(self):

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        data = json.loads(self.rfile.read(content_length).decode())

        path = self.path

        if path.startswith("/api"):
            endpoints = RequestHandler.endpoints

            path = path[4:]

            index = path.find("/", 1)
            if index == -1:
                endpoint = path
            else:
                endpoint = path[:index]

            try:
                code = 200
                content_type = "application/json"
                expires = True
                print(endpoint)
                contents = endpoints[endpoint].handle_request(self, RequestHandler.server, data)

                account = None
                print(contents)
                if "session" in contents.keys():
                    try:
                        print("loaded session from login")
                        account = Account.sessions[contents["session"]]
                        expires = False
                    except KeyError:
                        print("session not found: " + contents["session"])
                        print(Account.sessions)

                self._set_headers(account, code, content_type, expires)
                self.wfile.write(str.encode(json.dumps(contents)))
            except KeyError as e:
                print(e)
                self.send_error(404,'File Not Found: %s' % self.path)

        
def start_webserver(server):
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RequestHandler)

    os.chdir("../web")

    RequestHandler.server = server
    RequestHandler.endpoints = {
        "/activeclients": ActiveClientsEndpoint(),
        "/clientinfo": ClientInfoEndpoint(),
        "/login": LoginEndpoint(),
        "/signup": SignupEndpoint(),
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