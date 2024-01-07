import os
import random
import configparser
from moviepy.editor import VideoFileClip

class BackgroundService:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.out = config['VideoService']['video_dir']
        self.video_dir = config['Background']['background_dir']
        self.cropped_width = int(config['Background']['cropped_width'])
        self.cropped_height = int(config['Background']['cropped_height'])
    
    def __crop_video_center(self) -> VideoFileClip:
        video_clip: VideoFileClip = self.__get_random_video()
        center_x: int = (video_clip.size[0] // 2) - (self.cropped_width // 2)
        center_y: int = (video_clip.size[1] // 2) - (self.cropped_height // 2)

        cropped_video: VideoFileClip = video_clip.crop(center_x, center_y, center_x + self.cropped_width, center_y + self.cropped_height)
        return cropped_video

    def get_background(self, duration) -> VideoFileClip:
        video_clip: VideoFileClip = self.__crop_video_center()
        start, end = self.__get_random_slice(video_clip.duration, duration)
        video_clip = video_clip.subclip(start, end)
        video_clip = video_clip.without_audio()
        return video_clip

    def __get_random_slice(self, total_duration: int, target_duration: int):
        max_end = int(total_duration - target_duration)
        start = random.randint(0, max_end)

        return start, start + target_duration

    def __get_random_video(self) -> VideoFileClip:
        files = [os.path.join(self.video_dir, f) for f in os.listdir(self.video_dir) if os.path.isfile(os.path.join(self.video_dir, f))]
        if files:
            random_file = random.choice(files)
            return VideoFileClip(random_file)
        else:
            return None


bs: BackgroundService = BackgroundService()
# bs.crop_video_center()
# bs.get_random_video()