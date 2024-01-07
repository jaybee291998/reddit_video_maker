from dataclasses import dataclass

@dataclass
class ScreenshotRequest:
    id: str
    url: str
    handle: str
    file_name: str
    folder_name: str

    # no args contructor
    def __init__(self):
        url = None
        handle = None
        file_name = None
        folder_name = None
        id = None
