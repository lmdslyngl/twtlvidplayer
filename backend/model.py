
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


class Video:
    def __init__(
            self,
            tweet_id: int,
            author_name: str,
            author_screen_name: str,
            author_thumbnail_url: str,
            retweeted_author_name: Optional[str],
            retweeted_author_screen_name: Optional[str],
            body: str,
            created_at: datetime,
            video_url: str,
            video_type: VideoType) -> None:

        self.tweet_id = tweet_id
        self.author_name = author_name
        self.author_screen_name = author_screen_name
        self.author_thumbnail_url = author_thumbnail_url
        self.retweeted_author_name = retweeted_author_name
        self.retweeted_author_screen_name = retweeted_author_screen_name
        self.body = body
        self.created_at = created_at
        self.video_url = video_url
        self.video_type = video_type

    @staticmethod
    def init_table() -> None:
        sql = """
            CREATE TABLE videolist(
                tweet_id INTEGER PRIMARY KEY,
                author_name TEXT,
                author_screen_name TEXT,
                author_thumbnail_url TEXT,
                retweeted_author_name TEXT,
                retweeted_author_screen_name TEXT,
                body TEXT,
                created_at INTEGER,
                video_url TEXT,
                video_type INTEGER)
        """
        con = TransactionManager.get_connection()
        con.execute(sql)

    @staticmethod
    def from_row(row: sqlite3.Row) -> "Video":
        return Video(
            tweet_id=row["tweet_id"],
            author_name=row["author_name"],
            author_screen_name=row["author_screen_name"],
            author_thumbnail_url=row["author_thumbnail_url"],
            retweeted_author_name=row["retweeted_author_name"],
            retweeted_author_screen_name=row["retweeted_author_screen_name"],
            body=row["body"],
            created_at=datetime.fromtimestamp(row["created_at"]),
            video_url=row["video_url"],
            video_type=row["video_type"])

    def to_dict(self) -> dict:
        return {
            "tweet_id": str(self.tweet_id),
            "author_name": self.author_name,
            "author_screen_name": self.author_screen_name,
            "author_thumbnail_url": self.author_thumbnail_url,
            "retweeted_author_name": self.retweeted_author_name,
            "retweeted_author_screen_name": self.retweeted_author_screen_name,
            "body": self.body,
            "created_at": self.created_at.timestamp(),
            "video_url": self.video_url,
            "video_type": int(self.video_type)
        }

    def insert(self) -> None:
        sql = """
            INSERT OR REPLACE INTO videolist (
                tweet_id,
                author_name,
                author_screen_name,
                author_thumbnail_url,
                retweeted_author_name,
                retweeted_author_screen_name,
                body,
                created_at,
                video_url,
                video_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        con = TransactionManager.get_connection()
        con.execute(sql, (
            self.tweet_id,
            self.author_name,
            self.author_screen_name,
            self.author_thumbnail_url,
            self.retweeted_author_name,
            self.retweeted_author_screen_name,
            self.body,
            self.created_at.timestamp(),
            self.video_url,
            int(self.video_type)))

    @staticmethod
    def select_since(since_id: int = None, count: int = None) -> List["Video"]:
        sql = """
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
            CREATE TABLE config(key TEXT PRIMARY KEY, value TEXT)
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

