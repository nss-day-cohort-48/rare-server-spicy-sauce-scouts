
import sqlite3
import json
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

def get_posts_by_user(user_id):
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
        WHERE p.user_id = ?
        """, (user_id, ))

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
                post = POST(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['image_url'],row['content'], row['approved'])
                posts.append(post.__dict__)
                
                
def get_posts_by_tag(tag_id):
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
            p.approved,
            pt.id,
            pt.post_id,
            pt.tag_id,
            t.id,
            t.label
        FROM PostTags pt
        JOIN Posts p
            on p.id = pt.post_id
        JOIN Tags t
            on t.id = pt.tag_id
        WHERE t.id = ?
        """, (tag_id, ))

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
                user_id = ?,
                category_id = ?,
                title =?,
                publication_date = ?,
                image_url = ?,
                content = ?,
                approved = ?
            WHERE id = ?
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'],
        new_post['image_url'], new_post['content'], new_post['approved'], id, ))

        rows_affected = db_cursor.rowcount

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
            (?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'],
        new_post['image_url'], new_post['content'], new_post['approved'], ))

        id = db_cursor.lastrowid

        new_post['id'] = id

        for tag_id in new_post['tags']:
            db_cursor.execute("""
            INSERT INTO PostTags
                (post_id, tag_id)
            VALUES (?,?)
            """, (new_post['id'], tag_id, ))

    return json.dumps(new_post)

def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))

def get_all_posts():
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
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
                post = POST(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['image_url'],row['content'], row['approved'])

                db_cursor.execute("""
                SELECT
                    t.id,
                    t.label
                FROM Tags t
                JOIN PostTags pt
                    on t.id = pt.tag_id
                JOIN Posts p on pt.post_id = p.id
                WHERE p.id = ?
                """, (post.id, ))

                tag_rows = db_cursor.fetchall()

                for tag_row in tag_rows:
                    tag = {
                        'id': tag_row['id'],
                        'label': tag_row['label']
                    }
                    post.tags.append(tag)


                posts.append(post.__dict__)

        return json.dumps(posts)


def get_single_post(id):
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
        WHERE p.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        post = POST(data['id'], data['user_id'], data['category_id'], data['title'], data['publication_date'], data['image_url'], data['content'], data['approved'])

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        JOIN PostTags pt
            on t.id = pt.tag_id
        JOIN Posts p on pt.post_id = p.id
        WHERE p.id = ?
        """, (post.id, ))

        tag_rows = db_cursor.fetchall()

        for tag_row in tag_rows:
            tag = {
                'id': tag_row['id'],
                'label': tag_row['label']
                }
            post.tags.append(tag)

    return json.dumps(post.__dict__)

