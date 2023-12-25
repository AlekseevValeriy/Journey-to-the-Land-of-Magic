import os
from os import listdir

# .py files
print('python files')
my_excepts = ['__pycache__', 'get_lines_quality.py', '__init__.py']
lines_quality = 0

for file in listdir():
    if file not in my_excepts:
        with open(file, 'r', encoding='utf8') as read_file:
            file_len = len(read_file.read().split('\n'))
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
