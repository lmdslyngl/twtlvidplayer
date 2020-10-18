
from typing import Iterable

class ExcludeByRetweetedAuthorScreenName:
    def __init__(self, screen_name_list: Iterable[str]) -> None:
        self.screen_name_list = set(screen_name_list)

    def __call__(self, tweet: dict) -> bool:
        return tweet["retweeted_author_screen_name"] not in self.screen_name_list
