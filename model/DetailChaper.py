class DetailChapter:
    def __init__(self, chapter_number, link):
        self.chapter_number = chapter_number
        self.link = link

    def __str__(self):
        return f"Chapter {self.chapter_number}: {self.link}"