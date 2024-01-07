from dataclasses import dataclass

@dataclass
class VoiceRequest:
    id: str
    text: str
    file_name: str
    folder_name: str

    def __init__(self):
        self.id = None
        self.text = None
        self.file_name = None
        self.folder_name = None