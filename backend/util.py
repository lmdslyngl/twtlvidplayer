
import sys
import json
from functools import lru_cache
from datetime import datetime, timedelta
import logging
from typing import Any, Callable


def init_logger() -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    stdout_handler = logging.StreamHandler(sys.stdout)
    root_logger.addHandler(stdout_handler)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    stdout_handler.setFormatter(formatter)

    # werkzeug_logger = logging.getLogger("werkzeug")
    # werkzeug_logger.disabled = True


@lru_cache(maxsize=1)
def load_config() -> dict:
    with open("config.json", "r") as f:
        return json.load(f)


def twitter_date_to_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%a %b %d %H:%M:%S +0000 %Y")


class TimedCachedFuncWrapper:
    def __init__(self, func, expire_duration=timedelta(seconds=10)):
        self.func = func
        self.expire_duration = expire_duration
        self.cache = {}

    def __call__(self, *args, **kwargs):
        cache_key = (*args, *tuple(kwargs.items()))
        try:
            cached_value, cached_timestamp = self.cache[cache_key]
            if self.expire_duration < datetime.now() - cached_timestamp:
                raise KeyError("Cache expired")
            return cached_value

        except KeyError:
            ret = self.func(*args, **kwargs)
            self.cache[cache_key] = (ret, datetime.now())
            return ret
