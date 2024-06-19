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
