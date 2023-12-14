from os import listdir

my_excepts = ['__pycache__', 'get_lines.py']
lines_quality = 0

for file in listdir():
    if file not in my_excepts:
        with open(file, 'r', encoding='utf8') as read_file:
            lines_quality += len(read_file.read().split('\n'))
print(lines_quality)
