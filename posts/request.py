import sqlite3
import json
from sqlite3.dbapi2 import connect
from models import POST

def get_posts_by_subscription(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT *
            FROM Users
            JOIN Subscriptions
            ON Users.id = Subscriptions.follower_id
            JOIN Posts
            ON Posts.user_id = Subscriptions.author_id
            WHERE Subscriptions.follower_id = ?
        """, (id, ))

        original_posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
                post = POST(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['image_url'],row['content'], row['approved'])
                original_posts.append(post.__dict__)

                posts = []

        for i in original_posts:
            if i not in posts:
                posts.append(i)

    return json.dumps(posts)

def get_posts_by_category(category_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM Posts p
        WHERE p.category_id = ?
        """, (category_id, ))

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
                post = POST(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['image_url'],row['content'], row['approved'])
                posts.append(post.__dict__)
    return json.dumps(posts)

def update_post(id, new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Posts
            SET
                user_id = ?
                category_id = ?
                title =?
                publication_date = ?
                image_url = ?
                content = ?
                approved = ?
            WHERE id = ?
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'],
        new_post['image_url'], new_post['content'], new_post['approved'], id, ))

        rows_affected = db_cursor.row_count

    if rows_affected == 0:
        return False
    else: 
        return True

def create_post(new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            (user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES
            (?, ?, ?, ?, ?, ?, ?):
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'],
        new_post['image_url'], new_post['content'], new_post['approved'], ))

        id = db_cursor.lastrowid
        new_post['id'] = id

    return json.dumps(new_post)

def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))