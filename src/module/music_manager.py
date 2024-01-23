from pygame.mixer import Sound, Channel

from json_reader import JsonReader


class FullError(Exception):
    '''Класс ошибки переполнения стака каналов'''

    def __init__(self):
        pass


class MusicManager:
    '''Класс менеджера музыки'''
    ID_EFFECTS = (0, 4)
    ID_MUSICS = (4, 8)
    ID_ALL = (0, 8)

    sound_stack = []

    paths = JsonReader.read_file("..//..//data//json//music.json")
    music_storage = paths['music']
    effect_storage = paths['effect']

    def __init__(self, volume=1) -> None:
        self.volume = volume

        if len(MusicManager.sound_stack) != 0:
            MusicManager.sound_stack = []
        for n in range(MusicManager.ID_ALL[1]):
            MusicManager.sound_stack.append(Channel(n))
        for key in MusicManager.music_storage:
            MusicManager.music_storage[key] = Sound(MusicManager.music_storage[key])

        for key in MusicManager.effect_storage:
            MusicManager.effect_storage[key] = Sound(MusicManager.effect_storage[key])

    def set_volume(self, volume: int) -> None:
        '''Метод установки громкости для эффектов и музыки'''
        self.volume = volume
        for sound in MusicManager.sound_stack:
            sound.set_volume(self.volume)

    def stop_sound(self, sound_type: str) -> None:
        '''Метод для остановки звуков'''
        if sound_type == 'music':
            sound_range = MusicManager.ID_MUSICS
        elif sound_type == 'effect':
            sound_range = MusicManager.ID_EFFECTS
        else:
            sound_range = MusicManager.ID_ALL

        _ = [MusicManager.sound_stack[n].stop() for n in range(*sound_range)]

    def activate_effect(self, effect_name: str) -> None:
        '''Метод для активации эффектов'''
        try:
            free, free_id = self.is_free(MusicManager.ID_EFFECTS)
            if free:
                MusicManager.sound_stack[free_id].play(MusicManager.effect_storage[effect_name], loops=0)
                MusicManager.sound_stack[free_id].set_volume(self.volume)
            else:
                raise FullError
        except FullError:
            # print(f"Error. Type: Effect. Sound: {effect_name}. message: stack is full.")
            pass
        except Exception as error:
            # print(error)
            # print(error.__class__, error.__traceback__)
            pass

    def activate_music(self, music_name: str) -> None:
        '''Метод для активации музыки'''
        try:
            free, free_id = self.is_free(MusicManager.ID_MUSICS)
            if free:
                MusicManager.sound_stack[free_id].play(MusicManager.music_storage[music_name], loops=-1)
                MusicManager.sound_stack[free_id].set_volume(self.volume)
            else:
                raise FullError
        except FullError:
            # print(f"Error. Type: Music. Sound: {music_name}. message: stack is full.")
            pass
        except Exception as error:
            # print(error)
            # print(error.__class__, error.__traceback__)
            pass

    def is_free(self, id_type: int) -> tuple:
        '''Метод проверки свободных каналов'''
        free = False
        free_id = -1
        for n in range(*id_type):
            if not MusicManager.sound_stack[n].get_busy():
                free = True
                if free_id == -1:
                    free_id = n
        return free, free_id
