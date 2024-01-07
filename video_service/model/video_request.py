from dataclasses import dataclass
from .frame import Frame
@dataclass
class VideoRequest:
    file_name: str
    folder_name: str
    background_video_path: str
    frames: list[Frame]

    def __init__(self, file_name: str, folder_name: str, background_video_path: str):
        self.file_name = file_name
        self.folder_name = folder_name
        self.background_video_path = background_video_path
        self.frames = []

    def addFrame(self, frame: Frame):
        self.frames.append(frame)