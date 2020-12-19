
from typing import Optional, List
from enum import IntEnum, auto
from datetime import datetime
from contextlib import contextmanager
import threading
import sqlite3
from pathlib import Path


class TransactionManager:
    @classmethod
    def get_threadlocal(cls) -> dict:
        if not hasattr(cls, "local"):
            cls.local = threading.local()
        return cls.local

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        local = cls.get_threadlocal()
        if hasattr(local, "con"):
            return local.con
        else:
            con = sqlite3.connect("data/vid.db")
            con.row_factory = sqlite3.Row
            local.con = con
            return con

    @classmethod
    @contextmanager
    def transaction(cls) -> None:
        cls.get_connection().execute("BEGIN")
        yield
        cls.get_connection().commit()

    @classmethod
    def begin(cls) -> None:
        cls.get_connection().execute("BEGIN")

    @classmethod
    def commit(cls) -> None:
        cls.get_connection().commit()


class VideoType(IntEnum):
    TWITTER = auto()
    SOUNDCLOUD = auto()
    YOUTUBE = auto()


class User:
    def __init__(
            self,
            user_id: int,
            name: str,
            screen_name: str,
            thumbnail_url: str) -> None:

        self.user_id = user_id
        self.name = name
        self.screen_name = screen_name
        self.thumbnail_url = thumbnail_url

    @staticmethod
    def init_table() -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                screen_name TEXT,
                thumbnail_url TEXT)
        """
        con = TransactionManager.get_connection()
        con.execute(sql)

    @staticmethod
    def from_row(row: sqlite3.Row, prefix: str = "") -> "User":
        return User(
            user_id=row[prefix + "user_id"],
            name=row[prefix + "name"],
            screen_name=row[prefix + "screen_name"],
            thumbnail_url=row[prefix + "thumbnail_url"])

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "screen_name": self.screen_name,
            "thumbnail_url": self.thumbnail_url
        }

    def insert(self) -> None:
        sql = """
            INSERT OR REPLACE INTO users(
                user_id,
                name,
                screen_name,
                thumbnail_url)
            VALUES (?, ?, ?, ?)
        """

        con = TransactionManager.get_connection()
        con.execute(sql, (
            self.user_id, self.name,
            self.screen_name, self.thumbnail_url))


class Video:
    def __init__(
            self,
            tweet_id: int,
            author: User,
            retweeted_user: Optional[User],
            body: str,
            created_at: datetime,
            video_url: str,
            video_type: VideoType) -> None:

        self.tweet_id = tweet_id
        self.author = author
        self.retweeted_user = retweeted_user
        self.body = body
        self.created_at = created_at
        self.video_url = video_url
        self.video_type = video_type

    @staticmethod
    def init_table() -> None:
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
        con = TransactionManager.get_connection()
        con.execute(sql)

    @staticmethod
    def from_row(row: sqlite3.Row) -> "Video":
        author = User.from_row(row, prefix="author_")
        if row["retweeter_user_id"] is None:
            retweeted_user = None
        else:
            retweeted_user = User.from_row(row, prefix="retweeter_")

        return Video(
            tweet_id=row["tweet_id"],
            author=author,
            retweeted_user=retweeted_user,
            body=row["body"],
            created_at=datetime.fromtimestamp(row["created_at"]),
            video_url=row["video_url"],
            video_type=row["video_type"])

    def to_dict(self) -> dict:
        d = {
            "tweet_id": str(self.tweet_id),
            "author_name": self.author.name,
            "author_screen_name": self.author.screen_name,
            "author_thumbnail_url": self.author.thumbnail_url,
            "body": self.body,
            "created_at": self.created_at.timestamp(),
            "video_url": self.video_url,
            "video_type": int(self.video_type)
        }

        if self.retweeted_user is not None:
            d["retweeted_author_name"] = self.retweeted_user.name
            d["retweeted_author_screen_name"] = self.retweeted_user.screen_name
        else:
            d["retweeted_author_name"] = None
            d["retweeted_author_screen_name"] = None

        return d

    def insert(self) -> None:
        con = TransactionManager.get_connection()

        self.author.insert()
        if self.retweeted_user is not None:
            self.retweeted_user.insert()

        sql = """
            INSERT OR REPLACE INTO videolist (
                tweet_id,
                author_user_id,
                retweeted_user_id,
                body,
                created_at,
                video_url,
                video_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        con.execute(sql, (
            self.tweet_id,
            self.author.user_id,
            None if self.retweeted_user is None else self.retweeted_user.user_id,
            self.body,
            self.created_at.timestamp(),
            self.video_url,
            int(self.video_type)))

    @staticmethod
    def select_since(since_id: int = None, count: int = None) -> List["Video"]:
        sql = """
            SELECT
                videolist.tweet_id      AS tweet_id,
                videolist.body          AS body,
                videolist.created_at    AS created_at,
                videolist.video_url     AS video_url,
                videolist.video_type    AS video_type,
                author.user_id          AS author_user_id,
                author.name             AS author_name,
                author.screen_name      AS author_screen_name,
                author.thumbnail_url    AS author_thumbnail_url,
                retweeter.user_id       AS retweeter_user_id,
                retweeter.name          AS retweeter_name,
                retweeter.screen_name   AS retweeter_screen_name,
                retweeter.thumbnail_url AS retweeter_thumbnail_url
            FROM videolist
                INNER JOIN users author
                    ON videolist.author_user_id = author.user_id
                LEFT OUTER JOIN users retweeter
                    ON videolist.retweeted_user_id = retweeter.user_id
            {}
            ORDER BY tweet_id ASC
            {}
        """

        placeholders = []
        if since_id is None:
            where_clause = ""
        else:
            where_clause = "WHERE ? <= tweet_id"
            placeholders.append(since_id)

        if count is None:
            limit_clause = ""
        else:
            limit_clause = "LIMIT ?"
            placeholders.append(count)

        sql = sql.format(where_clause, limit_clause)
        con = TransactionManager.get_connection()
        cursor = con.execute(sql, placeholders)
        return [Video.from_row(row) for row in cursor]

    @staticmethod
    def select_until(until_id: int = None, count: int = None) -> List["Video"]:
        sql = """
            SELECT
                videolist.tweet_id      AS tweet_id,
                videolist.body          AS body,
                videolist.created_at    AS created_at,
                videolist.video_url     AS video_url,
                videolist.video_type    AS video_type,
                author.user_id          AS author_user_id,
                author.name             AS author_name,
                author.screen_name      AS author_screen_name,
                author.thumbnail_url    AS author_thumbnail_url,
                retweeter.user_id       AS retweeter_user_id,
                retweeter.name          AS retweeter_name,
                retweeter.screen_name   AS retweeter_screen_name,
                retweeter.thumbnail_url AS retweeter_thumbnail_url
            FROM videolist
                INNER JOIN users author
                    ON videolist.author_user_id = author.user_id
                LEFT OUTER JOIN users retweeter
                    ON videolist.retweeted_user_id = retweeter.user_id
            {}
            ORDER BY tweet_id DESC
            {}
        """

        placeholders = []
        if until_id is None:
            where_clause = ""
        else:
            where_clause = "WHERE tweet_id <= ?"
            placeholders.append(until_id)

        if count is None:
            limit_clause = ""
        else:
            limit_clause = "LIMIT ?"
            placeholders.append(count)

        sql = sql.format(where_clause, limit_clause)
        con = TransactionManager.get_connection()
        cursor = con.execute(sql, placeholders)
        return reversed([Video.from_row(row) for row in cursor])


class Config:
    @staticmethod
    def init_table() -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS config(key TEXT PRIMARY KEY, value TEXT)
        """
        con = TransactionManager.get_connection()
        con.execute(sql)

    @staticmethod
    def insert(key: str, value: str) -> None:
        sql = """
            INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)
        """
        con = TransactionManager.get_connection()
        with TransactionManager.transaction():
            con.execute(sql, (key, value))

    @staticmethod
    def select(key: str) -> Optional[str]:
        sql = """
            SELECT value FROM config WHERE key = ?
        """
        con = TransactionManager.get_connection()
        cursor = con.execute(sql, (key,))

        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return row["value"]

