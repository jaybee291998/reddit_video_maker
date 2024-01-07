import os
import configparser
from .model.frame import Frame
from .model.video_request import VideoRequest
from moviepy.editor import VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, AudioFileClip, concatenate_videoclips


class VideoService:
    
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("settings.ini")
        self.video_dir = config['VideoService']['video_dir']
    
    def create_frame_clip(self, frame: Frame) -> ImageClip:
        audio_clip: AudioFileClip = AudioFileClip(frame.audio_path)
        image_clip: ImageClip = ImageClip(frame.image_path, duration=audio_clip.duration)
        image_clip = image_clip.set_audio(audio_clip)
        return image_clip

    def create_video_clip(self, video_request: VideoRequest) -> str:
        background_clip: VideoFileClip = VideoFileClip(video_request.background_video_path)
        
        image_clips: ImageClip = concatenate_videoclips([self.create_frame_clip(frame) for frame in video_request.frames])

        center_position = (background_clip.size[0] // 2 - image_clips.size[0] // 2, background_clip.size[1] // 2 - image_clips.size[1] // 2)
        image_clips = image_clips.set_position(center_position)

        background_clip = background_clip.subclip(0, image_clips.duration)
        background_clip = background_clip.without_audio()

        video_clip: CompositeVideoClip = CompositeVideoClip(clips=[background_clip, image_clips])

        base_path: str = f'{self.video_dir}/{video_request.folder_name}'

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        full_path: str = f'{base_path}/{video_request.file_name}.mp4'

        video_clip.write_videofile(full_path)
        return full_path

