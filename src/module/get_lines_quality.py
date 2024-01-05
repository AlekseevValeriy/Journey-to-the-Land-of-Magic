import os
from os import listdir

# .py files
print(f'python files WITHOUT space and #"' + "'")
my_excepts = ['__pycache__', 'get_lines_quality.py', '__init__.py']
lines_quality = 0

for file in listdir():
    if file not in my_excepts:
        with open(file, 'r', encoding='utf8') as read_file:
            file_text = tuple(filter(lambda a: len(a.lstrip()) > 0 and a.lstrip().lstrip()[0] not in ['"', "'", '#'],
                                     read_file.read().split('\n')))
            file_len = len(file_text)
            lines_quality += file_len
            print(f'{file} -> {file_len}')
print('------------------------------')
print(f'all files -> {lines_quality}')
print()
print()
print('------------------------------')
print(f'python files WITH space and #"' + "'")
lines_quality = 0

for file in listdir():
    if file not in my_excepts:
        with open(file, 'r', encoding='utf8') as read_file:
            file_text = read_file.read().split('\n')
            file_len = len(file_text)
            lines_quality += file_len
            print(f'{file} -> {file_len}')
print('------------------------------')
print(f'all files -> {lines_quality}')
print()
print()
print('------------------------------')
print('json files')

# .json files
os.chdir('..//..//data//json')
my_excepts = ['units_data.json']
lines_quality = 0

for file in listdir():
    if file not in my_excepts:
        with open(file, 'r', encoding='utf8') as read_file:
            file_len = len(read_file.read().split('\n'))
            lines_quality += file_len
            print(f'{file} -> {file_len}')
print('------------------------------')
print(f'all files -> {lines_quality}')
