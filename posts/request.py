import sqlite3
import json
from models import POST

def get_all_subscription_posts(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
        FROM subscriptions a
        WHERE a.follower_id = ?
        """, (id,))

        subscriptions = []

        dataset = db_cursor.fetchall()