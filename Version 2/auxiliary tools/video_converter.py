from moviepy.editor import *

import os


def converter():
    elements = os.listdir('videos')
    for element in elements:
        video = VideoFileClip(os.path.join('videos', f"{element[:-4]}.mp4"))
        video.audio.write_audiofile(os.path.join("sounds", f"{element[:-4]}.mp3"))


converter()
