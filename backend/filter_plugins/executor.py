
from typing import List, Callable
from data import filter_config

class FilterPluginExecutor:
    @classmethod
    def get_instance(cls) -> "FilterPluginExecutor":
        if hasattr(cls, "instance"):
            return cls.instance
        else:
            cls.instance = FilterPluginExecutor(filter_config.filters)
            return cls.instance

    def __init__(self, plugins: List[Callable[[], None]]) -> None:
        self.plugins = plugins

    def __call__(self, tweet_list: List[dict]) -> List[dict]:
        filtered_tweet_list = tweet_list
        for plugin in self.plugins:
            filtered_tweet_list = filter(plugin, filtered_tweet_list)
        return list(filtered_tweet_list)
