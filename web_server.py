from sys import argv
import os

from urllib.parse import urlparse

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer


class MyServer(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self._path_request = ''
        self._valid_path = False
        self._file_extension = ''

    def do_GET(self):
        print(f"1) client path request: {self.path}")
        self._path_request = self.path
        self._valid_path = self._parse_url()
        print(f"4 - Valid Path - {self._valid_path}")
        self._send_http_status()
        if self._valid_path:
            print("6")
            # self.send_header("Content-type", "text/html")
            self.send_header("Content-type", self._get_content_type())
            self.end_headers()
            print(f"7 - Header sent")
            self._get_file()
        print("10 - Not a valid path - file not sent")

    def _parse_url(self):
        print("Start: _parse_url")
        success = False
        self._is_root_path()
        parse_url_result = urlparse(self._path_request)  # Need a function to process these
        print(f"parse url {parse_url_result}")

        print(f"Before concat - self._path_request: {self._path_request}")
        self._path_request = os.getcwd() + self._path_request           # Put Working Dir path in a Config file can't use in init method.
        print(f"After concat - self._path_request: {self._path_request}")
        print("End: _parse_url")
        if os.path.exists(self._path_request) and self._file_extension_validator():
            success = True
        return success

    def _is_root_path(self):
        if self._path_request == "/" and len(self._path_request) == 1:
            print(f"2 - Path request is root - update")
            self._path_request = self._path_request + 'index.html'

    def _find_file_extension(self):
        url_file = self._path_request.split('/')[-1]
        print(f"url_file: {url_file}")
        return url_file.split('.')[-1]

    def _file_extension_validator(self):
        valid = False
        extension_list = ["html", "css", "js", "ico"]
        self._file_extension = self._find_file_extension()
        for extension in range(len(extension_list)):
            if extension_list[extension] == self._file_extension:
                print(f"file_extension: {self._file_extension}")
                valid = True
                break
        return valid

    def _get_content_type(self):
        content_type = {
            "html": "text/html",
            "css": "text/css",
            "js": "text/javascript",
            "ico": "text/html"  # Work around - trouble reading image file
        }
        return content_type[self._file_extension]

    def _send_http_status(self):
        """
        The correspond HTTP status is sent if the file path exists on the server or not - basic implementation
        :param: None
        :return: None
        """
        if self._valid_path:
            print("5 - send status resp")
            self.send_response(HTTPStatus.OK.value, HTTPStatus.OK.description)
        else:
            print("5 - send status err")
            self.send_response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.description)

    def _get_file(self):
        print("8")
        file_size = os.path.getsize(self._path_request)
        # file = open(self._path_request)
        with open(self._path_request) as file:
            file_data = file.read(file_size)
        self.wfile.write(bytes(file_data, 'utf-8'))
        print("9 - file sent to client")


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