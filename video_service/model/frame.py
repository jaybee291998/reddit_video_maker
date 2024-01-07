from dataclasses import dataclass

@dataclass
class Frame:
    id: str
    image_path: str
    audio_path: str

    def __init__(self):
        self.id = None
        self.image_path = None
        self.audio_path = None
    