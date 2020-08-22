
import sys
import json
from functools import lru_cache
from datetime import datetime
import logging


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
