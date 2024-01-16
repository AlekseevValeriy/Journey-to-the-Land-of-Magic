from pygame.mixer import music, Sound, Channel
from json_reader import JsonReader

class FullError(Exception):
    def __init__(self):
        pass

class MusicManager:
    ID_EFFECTS = (0, 4)
    ID_MUSICS = (4, 8)
    ID_ALL = (0, 8)

    sound_stack = list()

    paths = JsonReader.read_file("..//..//data//json//music.json")
    music_storage = paths['music']
    effect_storage = paths['effect']

    def __init__(self, volume=1):
        self.volume = volume
        for n in range(MusicManager.ID_ALL[1]):
            MusicManager.sound_stack.append(Channel(n))
        for key in MusicManager.music_storage:
            MusicManager.music_storage[key] = Sound(MusicManager.music_storage[key])

        for key in MusicManager.effect_storage:
            MusicManager.effect_storage[key] = Sound(MusicManager.effect_storage[key])

    def set_volume(self, volume):
        self.volume = volume
        for sound in MusicManager.sound_stack:
            sound.set_volume(self.volume)

    def stop_sound(self, sound_type):
        for n in range(*MusicManager.ID_MUSICS if sound_type == 'sound'
                        else MusicManager.ID_EFFECTS if sound_type == 'effect'
                        else MusicManager.ID_ALL):
            MusicManager.sound_stack[n].stop()

    def activate_effect(self, effect_name):
        try:
            free, free_id = self.is_free(MusicManager.ID_EFFECTS)
            if free:
                MusicManager.sound_stack[free_id].play(MusicManager.effect_storage[effect_name], loops=0)
                MusicManager.sound_stack[free_id].set_volume(self.volume)
            else:
                raise FullError
        except Exception as error:
            print(f"Error. Type: Effect. Sound: {effect_name}. message: stack is full.")

    def activate_music(self, music_name):
        try:
            free, free_id = self.is_free(MusicManager.ID_MUSICS)
            if free:
                MusicManager.sound_stack[free_id].play(MusicManager.music_storage[music_name], loops=-1)
                MusicManager.sound_stack[free_id].set_volume(self.volume)
            else:
                raise FullError
        except Exception as error:
            print(f"Error. Type: Music. Sound: {music_name}. message: stack is full.")

    def is_free(self, id_type):
        free = False
        free_id = -1
        for n in range(*id_type):
            if not MusicManager.sound_stack[n].get_busy():
                free = True
                if free_id == -1:
                    free_id = n
        return free, free_id
