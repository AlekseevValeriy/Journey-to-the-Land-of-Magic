from os import listdir

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
