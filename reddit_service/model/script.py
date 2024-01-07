from dataclasses import dataclass

from .entry import Entry

@dataclass
class Script:
    url: str
    submission: Entry
    folder_name: str
    comments: list[Entry]

    def __init__(self):
        self.url = ""
        self.submission = None
        self.folder_name = None
        self.comments = []

    def addComment(self, comment: Entry):
        self.comments.append(comment)