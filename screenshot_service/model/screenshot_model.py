from dataclasses import dataclass

@dataclass
class ScreenshotModel:
    id: str
    path: str

    #no args constructor
    def __init__(self):
        id = None
        path = None