import os


class FileController:
    def __init__(self):
        self._dir_path = ''
        print("Created")

    def set_dir_file_path(self, url_file_path: str):
        self._set_dir_file_path(url_file_path)

    def get_dir_file_path(self):
        return self._dir_path

    def file_exists(self):
        valid_cwd = os.path.exists(self._dir_path)
        print(f"valid_cwd: {valid_cwd}")
        valid_ext = self._file_extension_validator(self._get_file_extension())
        print(f"valid_ext: {valid_ext}")
        return valid_cwd and valid_ext

    def get_file(self):
        print("8")
        file_size = os.path.getsize(self._dir_path)
        with open(self._dir_path) as file:
            file_data = file.read(file_size)
        print("9 - file sent to client")
        return bytes(file_data, 'utf-8')

    def get_file_extension(self):
        file_extension = self._get_file_extension()
        if not self._file_extension_validator(file_extension):
            print("Invalid file extension")
        return file_extension

    def _set_dir_file_path(self, url_file_path):
        self._dir_path = os.getcwd() + url_file_path
        print(f"_set_dir_file_path: {self._dir_path}")

    def _get_file_extension(self):
        url_file_name = self._dir_path.split('/')[-1]
        print(f"url_file: {url_file_name}")
        return url_file_name.split('.')[-1]

    @staticmethod
    def _file_extension_validator(extension):
        valid_extension = False
        extension_list = ["html", "css", "js", "ico"]
        if extension in extension_list:
            valid_extension = True
        print(f"extension state: {valid_extension}")
        return valid_extension
