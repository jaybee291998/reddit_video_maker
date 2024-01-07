from dataclasses import dataclass

@dataclass
class VoiceModel:
    id: str
    path: str

    def __init__(self):
        self.id = None
        self.path = None