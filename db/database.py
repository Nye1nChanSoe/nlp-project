import sqlite3
from datetime import datetime

DB_PATH = "news.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                content TEXT,
                predicted_category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS seen_urls (
                url TEXT PRIMARY KEY
            );
        """
        )
        print("Database initialised")


def insert_article(article):
    with sqlite3.connect(DB_PATH) as conn:
        try:
            conn.execute(
                """
                INSERT INTO articles (url, title, content, predicted_category)
                VALUES (?, ?, ?, ?)
            """,
                (
                    article["url"],
                    article["title"],
                    article["content"],
                    article["predicted_category"],
                ),
            )
        except sqlite3.IntegrityError:
            # Duplicate URL = already scraped
            pass


def mark_url_seen(url: str):
    with sqlite3.connect(DB_PATH) as conn:
        try:
            conn.execute(
                """
                INSERT INTO seen_urls (url) VALUES (?)
            """,
                (url,),
            )
        except sqlite3.IntegrityError:
            pass


def get_unseen_links(all_links: list, limit: int = 5):
    if not all_links:
        return []
    with sqlite3.connect(DB_PATH) as conn:
        placeholders = ",".join("?" * len(all_links))
        query = f"SELECT url FROM seen_urls WHERE url IN ({placeholders})"
        seen = set(row[0] for row in conn.execute(query, all_links))
    unseen = [url for url in all_links if url not in seen]
    return unseen[:limit]


def get_all_articles():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT * FROM articles ORDER BY created_at DESC")
        return cursor.fetchall()


def update_prediction(article_id, category):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            UPDATE articles
            SET predicted_category = ?
            WHERE id = ?
        """,
            (category, article_id),
        )
