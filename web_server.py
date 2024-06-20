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
        # print(f"header_data: \n{self.headers}") # DBG
        content_type = self.headers['Content-Type']
        content_length = self.headers['Content-Length']
        content_form_type, temp_dict = cgi.parse_header(content_type)
        # print(f"Content Form Type: {content_form_type}") # DBG
        if content_form_type == 'multipart/form-data':
            # If in the HTML: enctype="multipart/form-data"
            # print("cgi.parse_multipart") # DBG
            post_data_header = {}
            boundary_in_bytes = bytes(temp_dict['boundary'], 'utf-8')  # convert boundary value from str to bytes.
            # print(f" post_data_header boundary value converted to bytes: {boundary_in_bytes}") # DBG
            post_data_header['boundary'] = boundary_in_bytes
            post_data_header['content-length'] = content_length
            # print(f"post_header_data: {post_data_header}") # DBG
            post_data = cgi.parse_multipart(self.rfile, post_data_header)
        else:
            # If in the HTML: enctype="application/x-www-form-urlencoded"
            # print("cgi.parse") # DBG
            post_data_header = {'REQUEST_METHOD': self.command,
                                'CONTENT_TYPE': content_type,
                                'CONTENT_LENGTH': content_length}
            post_data = cgi.parse(self.rfile, post_data_header)
        print(f"Received Post Data: {post_data}")
        #
        self.web_app = WebApplication()
        self.web_app.process_server_request(self.path)
        status_code, status_info = self.web_app.get_app_status_code()
        self.send_response(status_code, status_info)
        content_type, requested_data = self.web_app.get_app_data()
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(requested_data)
        #
        print(f"END: do_POST")


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
