import json
with open('../settings/buttons_start_menu.json', 'r') as file:
    data = json.load(file)

for button in data:
    print(data[button], button)