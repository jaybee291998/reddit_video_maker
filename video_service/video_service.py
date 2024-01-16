import os
import configparser
from .model.frame import Frame
from .model.video_request import VideoRequest
from moviepy.editor import VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx.resize import resize

from .background_service import BackgroundService

class VideoService:
    
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("settings.ini")
        self.video_dir = config['VideoService']['video_dir']
        self.image_clip_scale = float(config['VideoService']['image_clip_scale'])
        self.background_service: BackgroundService = BackgroundService()
    
    def create_frame_clip(self, frame: Frame) -> ImageClip:
        audio_clip: AudioFileClip = AudioFileClip(frame.audio_path)
        image_clip: ImageClip = ImageClip(frame.image_path, duration=audio_clip.duration)
        image_clip = image_clip.set_audio(audio_clip)
        return image_clip

    def create_video_clip(self, video_request: VideoRequest) -> str:

        image_clips: ImageClip = concatenate_videoclips([self.create_frame_clip(frame) for frame in video_request.frames if frame.image_path is not None and frame.audio_path is not None]) 
        background_clip: VideoFileClip = self.background_service.get_background(image_clips.duration)
        image_clips = resize(image_clips, self.image_clip_scale)
        center_position = (background_clip.size[0] // 2 - image_clips.size[0] // 2, background_clip.size[1] // 2 - image_clips.size[1] // 2)
        image_clips = image_clips.set_position(center_position)

        # background_clip = background_clip.subclip(0, image_clips.duration)
        # background_clip = background_clip.without_audio()

        video_clip: CompositeVideoClip = CompositeVideoClip(clips=[background_clip, image_clips])

        base_path: str = f'{self.video_dir}/{video_request.folder_name}'

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        full_path: str = f'{base_path}/{video_request.file_name}.mp4'

        video_clip.write_videofile(full_path)
        # background_clip.write_videofile(full_path)
        return full_path

