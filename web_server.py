from sys import argv
import os

from urllib.parse import urlparse

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

from file_management import FileController


class MyServer(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        # self._path_request = ''
        self._valid_path = False
        # self._file_extension = ''
        self._file_controller = FileController  # set object type as a FileController object

    def do_GET(self):
        print(f"1) client path request: {self.path}")
        # self._path_request = self.path
        self._file_controller = FileController()
        self._valid_path = self._parse_url()
        print(f"4 - Valid Path - {self._valid_path}")
        self._send_http_status()
        if self._valid_path:
            print("6")
            # self.send_header("Content-type", "text/html")
            self.send_header("Content-type", self._get_content_type())
            self.end_headers()
            print(f"7 - Header sent")
            file_data = self._file_controller.get_file()
            self.wfile.write(file_data)
        print("10 - Not a valid path - file not sent")

    def _parse_url(self):
        print("Start: _parse_url")
        # self._file_controller = FileController()
        url_data = urlparse(self.path)  # Need a function to process these
        print(f"parse url {url_data}")
        url_data_path = self._is_root_path(url_data.path)
        self._file_controller.set_dir_file_path(url_data_path)
        success = self._file_controller.file_exists()
        return success

    @staticmethod
    def _is_root_path(url_path):
        if url_path == "/" and len(url_path) == 1:
            print(f"2 - Path request is root - update")
            url_path = url_path + 'index.html'
        return url_path

    def _get_content_type(self):
        content_type = {
            "html": "text/html",
            "css": "text/css",
            "js": "text/javascript",
            "ico": "text/html"  # Work around - trouble reading image file
        }
        return content_type[self._file_controller.get_file_extension()]

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
