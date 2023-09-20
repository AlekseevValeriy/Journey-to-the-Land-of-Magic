import json
from os import path

"""
Класс, который считывает и записывает параметры с файлов .json
"""


class ParameterReaderRead:
    def __init__(self, file_name, file_path=''):
        self.file_name = file_name
        self.file_path = file_path

    def load_parameters(self):
        with open(path.join(self.file_path, self.file_name), 'r') as file:
            return json.load(file)


class ParameterReaderWrite:
    def __init__(self, file_name, *parameters, file_path=''):
        self.file_name = file_name
        self.file_path = file_path
        # параметры поступают в формате ['название параметра', изменение]
        self.parameters = parameters

    def upload_parameters(self):
        with open(path.join(self.file_path, self.file_name), 'r') as file:
            data = json.load(file)
        for name, change in self.parameters:
            data[name] = change
        with open(path.join(self.file_path, self.file_name), 'w') as file:
            json.dump(data, file)
