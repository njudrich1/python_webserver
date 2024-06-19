from urllib.parse import urlparse, parse_qs
import json
from http import HTTPStatus

from file_management import FileController


class WebApplication:
    def __init__(self):
        self._file_path = ''
        self.valid_file_path = False
        self._file_controller = FileController()

    def process_server_request(self, url_path):
        print(f"BEGIN: process_server_request")
        print(f"HTTP Server Received path: {url_path}")
        url_data = urlparse(url_path)
        # path = self._update_path_if_root(url_data.path) UNCOMMENT
        # print(f"Root Path: {url_path}")
        self._update_path(url_data.path)
        print(f"Updated path {self._file_path}")
        # self._set_requested_file_path(path)
        # print(f"_set_requested_file_path Path: {url_path}")
        self.valid_file_path = self._validate_url()
        print(f"Valid file path request?: {self.valid_file_path}")
        self._parse_query_string(url_data.query)
        print(f"END: process_server_request")

    def get_app_status_code(self):
        print(f"BEGIN: get_app_status_code")
        if self.valid_file_path:
            http_status_code = HTTPStatus.OK.value
            http_status_info = HTTPStatus.OK.description
        else:
            http_status_code = HTTPStatus.NOT_FOUND.value
            http_status_info = HTTPStatus.NOT_FOUND.description
        print(f"END: get_app_status_code")
        return http_status_code, http_status_info

    def get_app_data(self):
        print(f"BEGIN: get_app_data")
        if self.valid_file_path:
            content_type = self._get_content_type()
            requested_data = self._file_controller.get_file()
        else:
            print('File Not Found! - 404')
            self._file_controller.set_dir_file_path('/views/Not Found/page_not_found.html')
            content_type = self._get_content_type()
            requested_data = self._file_controller.get_file()
        print(f"END: get_app_data")
        return content_type, requested_data

    def _validate_url(self):
        self._file_controller.set_dir_file_path(self._file_path)  # Process URL path
        return self._file_controller.file_exists()

    def _set_requested_file_path(self, path):
        self._file_path = path

    def _update_path(self, path):
        print("BEGIN: _update_path")
        path = self._update_path_if_root(path)
        extension = self._file_controller.get_file_extension(path)
        print(f"Extension: {extension}")
        if extension == 'json':
            self._file_path = '/web_app/asserts/data' + path
        else:
            self._file_path = '/web_app/views' + path
        print(f"File Path: {self._file_path}")
        print("END: _update_path")

    @staticmethod
    def _update_path_if_root(path):
        if path == "/" and len(path) == 1:
            print(f"_update_path_if_root: Path is Root Update.")
            path = '/home/index.html'
        return path

    def _parse_query_string(self, query_string):
        print("BEGIN: _parse_query_string ")
        if not query_string == '' and self.valid_file_path:
            print(f"QS exists!")
            q_string_dict = parse_qs(query_string)
            file_path_list = self._file_path.split('/')
            file_path_list.remove(file_path_list[-1])
            file_directory = file_path_list[-1]
            print(f"Directory: {file_directory}")
            with open("./web_app/asserts/data/" + file_directory + "/data.json", "w") as outfile:
                print("Creating json file")
                json.dump(q_string_dict, outfile)
        print(f"END: _parse_query_string")

    def _get_content_type(self):
        content_type = {
            "html": "text/html",
            "css": "text/css",
            "js": "text/javascript",
            "json": "application/json",
            "ico": "text/html"  # Work around - trouble reading image file
        }
        return content_type[self._file_controller.get_file_extension(self._file_path)]
