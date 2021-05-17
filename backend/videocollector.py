
from typing import List, Optional
import sys
from datetime import datetime
import re
from logging import getLogger
import time

from twapi import get_home_timeline
from model import TransactionManager, Video, VideoType, User
from util import twitter_date_to_datetime, init_logger


def extract_video_tweets(twapi_search_response: dict) -> List[Video]:
    video_list = []

    for tweet in twapi_search_response:
        video_url_candidates = [
            get_video_url_from_tweet(tweet),
            get_soundcloud_url_from_tweet(tweet),
            get_youtube_url_from_tweet(tweet)
        ]
        video_types = [
            VideoType.TWITTER,
            VideoType.SOUNDCLOUD,
            VideoType.YOUTUBE
        ]

        # Twitterビデオ，SoundCloud，Youtubeのいずれか1つのURLを選択
        selected_video_url = None
        for video_url, video_type in zip(video_url_candidates, video_types):
            if video_url is not None:
                selected_video_url = video_url
                break

        # ビデオのURLが無かったときはこのツイートを無視
        if selected_video_url is None:
            continue

        if "retweeted_status" in tweet:
            # RTだった場合はRT元のツイートから情報を取得する
            rt = tweet["retweeted_status"]

            author = User(
                user_id=rt["user"]["id"],
                name=rt["user"]["name"],
                screen_name=rt["user"]["screen_name"],
                thumbnail_url=rt["user"]["profile_image_url_https"])

            retweeter = User(
                user_id=tweet["user"]["id"],
                name=tweet["user"]["name"],
                screen_name=tweet["user"]["screen_name"],
                thumbnail_url=tweet["user"]["profile_image_url_https"])

            vid = Video(
                tweet_id=tweet["id"],
                author=author,
                retweeted_user=retweeter,
                body=rt["full_text"],
                created_at=twitter_date_to_datetime(tweet["created_at"]),
                video_url=selected_video_url,
                video_type=video_type)

        else:
            author = User(
                user_id=tweet["user"]["id"],
                name=tweet["user"]["name"],
                screen_name=tweet["user"]["screen_name"],
                thumbnail_url=tweet["user"]["profile_image_url_https"])

            vid = Video(
                tweet_id=tweet["id"],
                author=author,
                retweeted_user=None,
                body=tweet["full_text"],
                created_at=twitter_date_to_datetime(tweet["created_at"]),
                video_url=selected_video_url,
                video_type=video_type)

        video_list.append(vid)

    return video_list


def get_video_url_from_tweet(tweet: dict) -> Optional[str]:
    if "extended_entities" not in tweet:
        return None

    entities = tweet["extended_entities"]
    if "media" not in entities:
        return None

    media_list = entities["media"]
    for media in media_list:
        if media["type"] == "video":
            video_info = media["video_info"]
            video_variants = video_info["variants"]

            # 一番ビットレートの高いvideo/mp4を選択
            video_selected = sorted(
                filter(lambda x: x["content_type"] == "video/mp4", video_variants),
                key=lambda x: x["bitrate"],
                reverse=True)[0]

            return video_selected["url"]

    return None


def get_urls_from_tweet(tweet: dict) -> List[str]:
    if "entities" not in tweet:
        return None

    entities = tweet["entities"]
    if "urls" not in entities:
        return None

    return [url["expanded_url"] for url in entities["urls"]]


def get_soundcloud_url_from_tweet(tweet: dict) -> Optional[str]:
    urls = filter(lambda x: "soundcloud.com" in x, get_urls_from_tweet(tweet))
    try:
        return next(urls)
    except StopIteration:
        return None


def get_youtube_url_from_tweet(tweet: dict) -> Optional[str]:
    urls = filter(lambda x: "youtube.com/watch" in x, get_urls_from_tweet(tweet))
    try:
        return next(urls)
    except StopIteration:
        pass

    # 短縮URL版を探す
    urls = filter(lambda x: "youtu.be" in x, get_urls_from_tweet(tweet))
    try:
        # 短縮URLを展開して返す
        url = next(urls)
        v = re.sub(r".*youtu\.be/(.*)", r"\1", url)
        return "https://www.youtube.com/watch?v=" + v
    except StopIteration:
        return None


def main():
    init_logger()
    logger = getLogger("videocollector")

    logger.info("started")

    while True:
        try:
            tweets = get_home_timeline()
            video_list = extract_video_tweets(tweets)

            with TransactionManager.transaction():
                for video in video_list:
                    video.insert()

            logger.info("fetched {} videos.".format(len(video_list)))

        except Exception as e:
            logger.exception(e)

        finally:
            time.sleep(10 * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
