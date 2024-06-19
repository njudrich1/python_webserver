import os


class FileController:
    def __init__(self):
        self._dir_path = ''
        print("Created")

    def set_dir_file_path(self, url_file_path: str):
        print(f"BEGIN: set_dir_file_path")
        self._set_dir_file_path(url_file_path)
        print(f"END: set_dir_file_path")

    def get_dir_file_path(self):
        print(f"get_dir_file_path")
        return self._dir_path

    def file_exists(self):
        print(f"BEGIN: file_exists")
        valid_cwd = os.path.exists(self._dir_path)
        print(f"valid_cwd: {valid_cwd}")
        valid_ext = self._file_extension_validator(self._get_file_extension(self._dir_path))
        print(f"valid_ext: {valid_ext}")
        print(f"END: file_exists")
        return valid_cwd and valid_ext

    def get_file(self):
        print(f"BEGIN: get_file")
        file_size = os.path.getsize(self._dir_path)
        with open(self._dir_path) as file:
            file_data = file.read(file_size)
        print("9 - file sent to client")
        print(f"END: get_file")
        return bytes(file_data, 'utf-8')

    def get_file_extension(self, file_path):
        print(f"BEGIN: get_file_extension")
        file_extension = self._get_file_extension(file_path)
        if not self._file_extension_validator(file_extension):
            print("Invalid file extension")
        print(f"END: get_file_extension")
        return file_extension

    def _set_dir_file_path(self, url_file_path):
        self._dir_path = os.getcwd() + url_file_path
        print(f"_set_dir_file_path: {self._dir_path} = {os.getcwd()} + {url_file_path}")

    @staticmethod
    def _get_file_extension(path):
        url_file_name = path.split('/')[-1]
        print(f"url_file: {url_file_name}")
        return url_file_name.split('.')[-1]

    @staticmethod
    def _file_extension_validator(extension):
        valid_extension = False
        extension_list = ["html", "css", "js", "json", "ico"]
        if extension in extension_list:
            valid_extension = True
        print(f"extension state: {valid_extension}")
        return valid_extension
