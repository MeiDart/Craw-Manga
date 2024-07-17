from model.DetailChaper import DetailChapter
from typing import List

class Manga:
    def __init__(self, name: str, chapters: int, detail_chapter: List['DetailChapter']) -> None:
        self.name = name
        self.chapters = chapters
        self.detail_chapter = detail_chapter

    def __str__(self):
        return f"Chapter {self.chapter_number}: {self.link}"