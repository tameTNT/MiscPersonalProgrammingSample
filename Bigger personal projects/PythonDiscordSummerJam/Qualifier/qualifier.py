"""
Use this file to write your solution for the Summer Code Jam 2020 Qualifier.

Important notes for submission:

- Do not change the names of the two classes included below. The test suite we
  will use to test your submission relies on existence these two classes.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the
  advanced requirements.

- Do not include "debug"-code in your submission. This means that you should
  remove all debug prints and other debug statements before you submit your
  solution.
"""
import datetime
import typing
from collections import Counter  # used in most_common_words method


class ArticleField:
    """The `ArticleField` class for the Advanced Requirements."""

    def __init__(self, field_type: typing.Type[typing.Any]):
        pass


class Article:
    """The `Article` class you need to write for the qualifier."""
    instance_num = 0  # new to me

    def __init__(self, title: str, author: str, publication_date: datetime.datetime, content: str):
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.last_edited = None
        self._content = content
        self.id = Article.instance_num
        Article.instance_num += 1

    def short_introduction(self, n_characters: int) -> str:
        # Finds the most recent, up to n_characters+1, occurrence of " " or "\n" in the content string
        latest_break = max(self.content.rfind(" ", 0, n_characters+1), self.content.rfind("\n", 0, n_characters+1))
        return self.content[:latest_break]

    def most_common_words(self, n_words: int) -> dict:
        s = self.content
        word_list = [""]
        for i in range(len(s)):  # essentially reconstructs content string omitting all non-alpha characters
            if s[i].isalpha():
                word_list[-1] += s[i].lower()
            else:
                word_list.append("")
        word_list = list(filter(None, word_list))  # removes empty strings

        word_counts = Counter(word_list).most_common(n_words)
        return dict(word_counts)

    def __repr__(self):
        return f"<Article title=\"{self.title}\" author='{self.author}' publication_date='{self.publication_date.isoformat()}'>"

    def __len__(self):
        return len(self.content)

    @property
    def content(self):  # new to me
        return self._content

    @content.setter
    def content(self, new_value):
        """Updates last_edited attribute each time content attribute is changed"""
        self._content = new_value
        self.last_edited = datetime.datetime.now()

    def __lt__(self, other):  # new to me
        """less than method implementation to allow for sorting of Articles by publication date"""
        return self.publication_date < other.publication_date
