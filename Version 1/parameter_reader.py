class ParameterReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.opened_file = ''
        self.file = ''
        self.parameters = {}

    def open_file(self):
        self.opened_file = open(self.file_name, 'r')
        self.file = self.opened_file.readlines()

    def close_file(self):
        if self.opened_file:
            self.opened_file.close()
            self.opened_file = ''
            self.file = ''

    def read_line(self, line, name_of_parameter):
        self.open_file()
        if 1 not in [len(line), len(name_of_parameter)]:
            for name, line_2 in zip(name_of_parameter, line):
                parameter = self.file[line_2].rstrip().lstrip('@').split('.')
                self.parameters[name] = [int(word) if word[0].isdigit() else word for word in parameter]
        elif 1 in [len(line), len(name_of_parameter)]:
            parameter = self.file[line].rstrip().lstrip('@').split('.')
            self.parameters[name_of_parameter] = [int(word) if word[0].isdigit() else word for word in parameter]
        self.close_file()

    def return_parameters(self):
        return self.parameters

if __name__ == '__main__':
    reader = ParameterReader('parameter.txt')
    reader.open_file()
    reader.read_line([3, 5 ,7], ['window', 'game_map', 'sector'])
    a = reader.return_parameters()
    print(a)