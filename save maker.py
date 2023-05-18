import shelve

class SaveMaker:
    def __init__(self, game_map=False, coordinate=False):
        self.map = game_map if game_map else list()
        self.coordinate = coordinate if coordinate else []

    def save(self):
        save_file = shelve.open('saves.txt')
        save_file['map_save'] = self.map
        save_file['coordinate_save'] = self.coordinate
        save_file.close()

    def read(self):
        save_file = shelve.open('saves.txt')
        game_map = save_file['map_save']
        coordinate = save_file['coordinate_save']
        save_file.close()
        return game_map, coordinate