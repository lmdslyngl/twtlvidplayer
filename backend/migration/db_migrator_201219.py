
"""
videolistテーブルに全部突っ込んでいたDBから，
Userテーブルを分離してDBへの移行スクリプト
"""

import sys
import sqlite3
from pathlib import Path
from contextlib import closing
import math
import json

import requests
import requests_oauthlib


def __get_auth() -> requests_oauthlib.OAuth1:
    with open("../data/token.json", "r") as f:
        token = json.load(f)

    return requests_oauthlib.OAuth1(
        client_key=token["api_key"],
        client_secret=token["api_secret"],
        resource_owner_key=token["access_token"],
        resource_owner_secret=token["access_token_secret"])


def get_screen_names(con):
    sql = """
        SELECT DISTINCT author_screen_name FROM videolist
        UNION
        SELECT DISTINCT retweeted_author_screen_name FROM videolist
    """

    with closing(con.cursor()) as cursor:
        cursor.execute(sql)
        return [row[0] for row in cursor.fetchall() if row[0] is not None]


def lookup_users_from_twitter_internal(screen_names):
    url = "https://api.twitter.com/1.1/users/lookup.json"
    params = {
        "screen_name": ",".join(screen_names)
    }

    r = requests.post(url, data=params, auth=__get_auth())
    if r.status_code == 420:
        raise Exception("Ratelimited: " + r.text)
    elif r.status_code == 200:
        return r.json()


def lookup_users_from_twitter(screen_names):
    users = []
    blocks_count = int(math.ceil(len(screen_names) / 100))

    for i in range(blocks_count):
        screen_names_block = screen_names[i * 100:min((i + 1) * 100, len(screen_names))]
        users.extend(lookup_users_from_twitter_internal(screen_names_block))

    return users


def init_new_db(con):
    sql = """
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            screen_name TEXT,
            thumbnail_url TEXT)
    """
    con.execute(sql)

    sql = """
        CREATE TABLE IF NOT EXISTS videolist(
            tweet_id INTEGER PRIMARY KEY,
            author_user_id INTEGER,
            retweeted_user_id INTEGER,
            body TEXT,
            created_at INTEGER,
            video_url TEXT,
            video_type INTEGER)
    """
    con.execute(sql)

    con.commit()


def insert_users(con, users):
    user_rows = [
        (user["id"], user["name"], user["screen_name"], user["profile_image_url_https"])
        for user in users]

    sql = """
        INSERT OR REPLACE INTO users(
            user_id,
            name,
            screen_name,
            thumbnail_url)
        VALUES (?, ?, ?, ?)
    """

    con.executemany(sql, user_rows)
    con.commit()


def transfer_videos(con_old, con_new):
    sql_old = """
        SELECT
            tweet_id,
            author_name,
            author_screen_name,
            author_thumbnail_url,
            retweeted_author_name,
            retweeted_author_screen_name,
            body,
            created_at,
            video_url,
            video_type
        FROM videolist
    """

    sql_new = """
        INSERT INTO videolist (
            tweet_id,
            author_user_id,
            retweeted_user_id,
            body,
            created_at,
            video_url,
            video_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    with closing(con_old.cursor()) as cur_old, closing(con_new.cursor()) as cur_new:
        cur_old.execute(sql_old)
        while True:
            row = cur_old.fetchone()
            if row is None:
                break

            sql_user_search = """
                SELECT user_id FROM users WHERE screen_name = ?
            """

            cur_new.execute(sql_user_search, (row["author_screen_name"],))
            author_user_id_row = cur_new.fetchone()
            author_user_id = None if author_user_id_row is None else author_user_id_row[0]

            cur_new.execute(sql_user_search, (row["retweeted_author_screen_name"],))
            retweeted_user_id_row = cur_new.fetchone()
            retweeted_user_id = None if retweeted_user_id_row is None else retweeted_user_id_row[0]

            new_row = (
                row["tweet_id"],
                author_user_id,
                retweeted_user_id,
                row["body"],
                row["created_at"],
                row["video_url"],
                row["video_type"])

            cur_new.execute(sql_new, new_row)

        con_new.commit()


def main():
    old_db_path = Path("vid.db")
    new_db_path = Path("vid_migrated.db")
    users_cache = Path("users.json")

    with closing(sqlite3.connect(old_db_path)) as con:
        screen_names = get_screen_names(con)

    if users_cache.exists():
        with open(users_cache, "r") as f:
            users = json.load(f)
    else:
        users = lookup_users_from_twitter(screen_names)
        with open(users_cache, "w") as f:
            json.dump(users, f)

    with closing(sqlite3.connect(new_db_path)) as con:
        con.row_factory = sqlite3.Row
        init_new_db(con)
        insert_users(con, users)

        with closing(sqlite3.connect(old_db_path)) as con_old:
            con_old.row_factory = sqlite3.Row
            transfer_videos(con_old, con)

    return 0


if __name__ == "__main__":
    sys.exit(main())
