import cgi
from urllib.parse import urlparse, parse_qs
from sys import argv
from http.server import BaseHTTPRequestHandler, HTTPServer

from web_app.web_application import WebApplication


class MyServer(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self._valid_path = False
        self.web_app = WebApplication

    def do_GET(self):
        print("----- BEGIN: GET Request -----")
        self.web_app = WebApplication()
        self.web_app.process_server_request(self.path)
        status_code, status_info = self.web_app.get_app_status_code()
        self.send_response(status_code, status_info)
        content_type, requested_data = self.web_app.get_app_data()
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(requested_data)
        print("----- END: Get -----")

    def do_POST(self):
        print(f"BEGIN: do_POST:")
        # boundary = {}     # TODO to handle 'multipart/form-data' forms
        # ctype, temp_dict = cgi.parse_header(self.headers['Content-Type'])
        # byte_boundary = bytes(temp_dict['boundary'], 'utf-8')
        # boundary['boundary'] = byte_boundary
        # content_type = (ctype; boundary)
        # print(self.headers['Content-Type'])
        # print(type(self.headers['Content-Type']))
        # exit(0)
        post_header_data = {'REQUEST_METHOD': self.command,
                            'CONTENT_TYPE': self.headers['Content-Type'],
                            'CONTENT_LENGTH': self.headers['Content-Length']}
        print(f"header_data: {self.headers}")
        print(f"post_header_data: {post_header_data}")
        post_data = cgi.parse(self.rfile, post_header_data)
        print(f"END: Post Data: {post_data}")

        # First Attempt - works!! ----
        # pdict = {}
        # ctype, temp_dict = cgi.parse_header(self.headers.get('content-type'))
        # print(f"ctype - cgi.parse_header : {ctype}")
        # print(f"temp_dict - cgi.parse_header : {temp_dict}")
        # byte_boundary = bytes(temp_dict['boundary'], 'utf-8')
        # print(f"pdict boundary convert to bytes: {byte_boundary}")
        # pdict['boundary'] = byte_boundary
        # print(f"{pdict}")
        # content_len = self.headers.get('Content-length')
        # print(f"Content-length: {content_len}")
        # pdict['content-length'] = content_len
        # print(f"{pdict}")
        # fields = cgi.parse_multipart(self.rfile, pdict)
        # print(f"cgi.parse_multipart: {fields}")


def run(http_server=HTTPServer, http_request_handler=MyServer, port_number=8000):
    host_name = 'localhost'  # Change in the future - hostname and port should come from a config file
    server_address = (host_name, port_number)
    web_server = http_server(server_address, http_request_handler)
    print("Server started http://%s:%s" % (host_name, port_number))
    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        web_server.server_close()
        print("Server stopped.")
    except Exception as e:
        web_server.server_close()
        print("Server stopped.")
        print(e)


if __name__ == "__main__":

    if len(argv) == 2:
        port = int(argv[1])  # hostname=localhost
        run(port_number=port)
    else:
        run()  # default hostname=localhost and port=8000
