from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
import xmlrpc

from file_server.web.account import Account
from file_server.web.endpoints.active_clients import ActiveClientsEndpoint
from file_server.web.endpoints.client_info import ClientInfoEndpoint
from file_server.web.endpoints.login import LoginEndpoint
from file_server.web.endpoints.logout import LogoutEndpoint
from file_server.web.endpoints.signup import SignupEndpoint
from file_server.web.endpoints.user import UserEndpoint
from file_server.web.endpoints.createauth import CreateAuthEndpoint
from file_server.web.endpoints.update_settings import UpdateSettingsEndpoint
from file_server.web.endpoints.directory_contents import DirectoryContentsEndpoint

import webbrowser

import os

import json

class RequestHandler(BaseHTTPRequestHandler):
    server = None

    def log_message(self, format, *args):
        return

    def _set_headers(self, account, code=200, content_type="text/html", expires=False):
        cookie_data = self.headers.get('Cookie')
        self.send_response(code)
        self.send_header('Content-type', content_type)

        if account is not None:
            self.send_header('Set-Cookie', 'session=' + account.session)

        if expires:
            self.send_header("Expires", "Mon, 01 Jan 1990 00:00:00 GMT")
        
        self.end_headers()

    def load_account_from_cookies(self):
        cookie_data = self.headers.get('Cookie')
        account = None
        if (cookie_data is not None):
            parsed_cookie = SimpleCookie(cookie_data)
            cookie = {}
            for c in parsed_cookie.values():
                cookie[c.key] = c.coded_value 

            if "session" in cookie and cookie["session"] != "":
                try:
                    account = Account.sessions[cookie.get("session")]
                except KeyError:
                    pass
        return account


    def handle_request(self, data):
        code = 200
        path = self.path
        endpoints = RequestHandler.endpoints
        account = self.load_account_from_cookies()
        expires = False
        contents = b""
        content_type = "text/html"


        try:
            if path.startswith("/api"):
                path = path[4:]

                index = path.find("/", 1)
                if index == -1:
                    endpoint_str = path
                else:
                    endpoint_str = path[:index]
                endpoint = endpoints[endpoint_str]

                if (endpoint.needs_auth and account is None):
                    code = 401
                    contents = b""
                else:
                    if data is None:
                        expires = True
                        data = -1
                        try: 
                            data = path[len(endpoint_str) + 1:]
                            data = int(data)
                        except (ValueError, IndexError) as e:
                            pass

                    #code = 403
                    content_type = "application/json"
                    contents = endpoint.handle_request(self, RequestHandler.server, account, data)

                    if hasattr(contents, "keys"):
                        if "session" in contents.keys():
                            try:
                                account = Account.sessions[contents["session"]]
                                expires = False
                            except KeyError:
                                print("Expected session to exist: " + contents["session"])

                        if "redirect" in contents.keys():
                            self.send_response(302)
                            self.send_header('Location', contents["redirect"])
                            self.end_headers()
                            return

                    contents = str.encode(json.dumps(contents))
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
                    self.send_response(302)
                    self.send_header('Location','/login')
                    self.end_headers()
                    return
                elif path == "/login" and account is not None:
                    self.send_response(302)
                    self.send_header('Location','/')
                    self.end_headers()
                    return
                else:
                    path = "/index.html"

                with open("." + path, "rb") as content_file:
                    contents = content_file.read()

            self._set_headers(account, code, content_type, expires)
            self.wfile.write(contents)

        except (IOError, KeyError) as e:
            print("exception: " + self.path)
            print(e)
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_GET(self):
        
        self.handle_request(None)

    def do_HEAD(self):
        self._set_headers(None)
        
    def do_POST(self):

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        data = self.rfile.read(content_length)
        data = json.loads(data.decode())

        self.handle_request(data)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):

    def __init__(self, server_address, requestHandler):
        HTTPServer.__init__(self, server_address, requestHandler)
        self.port = server_address[1]
        self.shutdown = False

    def serve_forever(self):
        if self.port == 8080:
            webbrowser.open('http://127.0.0.1:8080', new=2)

        while not self.shutdown:
            self.handle_request()

    def force_stop(self):
        self.server_close()
        self.shutdown = True
        self.create_dummy_request()

    def create_dummy_request(self):
        server = xmlrpcs.erver.SimpleXMLRPCServer('http://%s:%s' % self.server_address)
        server.ping()

def create_webserver(server, port=8080):
    server_address = ('', port)
    server = ThreadedHTTPServer(server_address, RequestHandler)

    os.chdir("../web")

    RequestHandler.server = server
    RequestHandler.endpoints = {
        "/activeclients": ActiveClientsEndpoint(),
        "/clientinfo": ClientInfoEndpoint(),
        "/login": LoginEndpoint(),
        "/logout": LogoutEndpoint(),
        "/signup": SignupEndpoint(),
        "/user": UserEndpoint(),
        "/createauth": CreateAuthEndpoint(),
        "/updatesettings": UpdateSettingsEndpoint(),
        "/directorycontents": DirectoryContentsEndpoint(),
    }

    

    return server
    