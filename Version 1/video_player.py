from moviepy.editor import *

class VideoPlayer:
    def __init__(self):
        self.video_dict = {}

    def add_video(self, video_name):
        self.video_dict[video_name] = VideoFileClip(video_name)

    def video_start(self, video_name):
        self.video_dict[video_name].preview()