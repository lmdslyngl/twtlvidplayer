
from datetime import datetime, timedelta
from typing import Iterable, Optional, List, Set
from twapi import get_lists, get_list_members
from util import TimedCachedFuncWrapper


class ExcludeByRetweetedAuthorScreenName:
    def __init__(self, screen_name_list: Iterable[str]) -> None:
        self.screen_name_list = set(screen_name_list)

    def __call__(self, tweet: dict) -> bool:
        return tweet["retweeted_author_screen_name"] not in self.screen_name_list


class ExcludeByTwitterList:
    def __init__(self, list_names: Iterable[str]) -> None:
        self.list_names = list_names
        self.get_exclude_user_screen_names_cached = TimedCachedFuncWrapper(
            self.get_exclude_user_screen_names,
            timedelta(seconds=30 * 60))

    def __call__(self, tweet: dict) -> bool:
        exclude_user_ids = self.get_exclude_user_screen_names_cached()
        return \
            tweet["author_screen_name"] not in exclude_user_ids \
            and tweet["retweeted_author_screen_name"] not in exclude_user_ids

    def get_exclude_user_screen_names(self) -> List[int]:
        list_ids = ExcludeByTwitterList.get_list_ids(self.list_names)
        return ExcludeByTwitterList.get_user_screen_names_in_lists(list_ids)

    @staticmethod
    def get_user_screen_names_in_lists(list_ids: List[int]) -> Set[int]:
        user_ids = set()
        for list_id in list_ids:
            list_members = get_list_members(list_id)
            list_member_ids = {member["screen_name"] for member in list_members}
            user_ids = user_ids.union(list_member_ids)
        return user_ids

    @staticmethod
    def get_list_ids(names: List[str]) -> List[int]:
        lists = get_lists()
        ids = []
        for name in names:
            try:
                list_id = next(filter(lambda x: x["name"] == name, lists))["id"]
                ids.append(list_id)
            except StopIteration:
                pass
        return ids

