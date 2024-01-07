from dataclasses import dataclass

@dataclass
class Entry:
    id: str
    body: str
    file_name: str
    handle: str
    title: str = "Unknown -uwu"