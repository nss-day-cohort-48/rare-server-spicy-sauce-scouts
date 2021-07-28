
import sqlite3
import json
from models import Tag, PostTag

def get_tags_by_post(post_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label,
            pt.tag_id
            pt.post_id
        FROM Tags t
        JOIN PostTags pt
            on pt.tag_id = t.id
        WHERE pt.post_id = ?
        """, (post_id, ))

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Tag(row['id'], row['post_id'], row['author_id'], row['content'])

            comments.append(comment.__dict__)

    return json.dumps(comments)


def get_tags_by_user (user_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            cm.id,
            cm.post_id,
            cm.author_id,
            cm.content
        FROM Comments cm
        WHERE cm.author_id = ?
        """, (user_id,))

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['post_id'], row['author_id'], row['content'])

            comments.append(comment.__dict__)

    return json.dumps(comments)


def create_tag(new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comments
            (post_id, author_id, content)
        VALUES
            ( ?, ?, ?);
        """, (new_comment['post_id'], new_comment['author_id'], new_comment['content'],))

        id = db_cursor.lastrowid

        new_comment['id'] = id

    return json.dumps(new_comment)
    

def delete_tag(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Comments
        WHERE id = ?
        """, (id, ))


def update_tag(id, new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Comments
            SET
                post_id = ?,
                author_id = ?,
                content = ?
        WHERE id = ?
        """, (new_comment['post_id'], new_comment['author_id'], new_comment['content'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


## this get_all is mainly for testing purposes.

def get_all_tags():
    """Gets all tags. Mainly for testing on this app"""
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            cm.id,
            cm.post_id,
            cm.author_id,
            cm.content
        FROM Comments cm
        """)

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            comment = Comment(row['id'], row['post_id'], row['author_id'], row['content'])

            comments.append(comment.__dict__)

    return json.dumps(comments)


def get_all_posttags():
    """Gets all posttags. Mainly for testing on this app"""
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            cm.id,
            cm.post_id,
            cm.author_id,
            cm.content
        FROM Comments cm
        """)

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            comment = Comment(row['id'], row['post_id'], row['author_id'], row['content'])

            comments.append(comment.__dict__)

    return json.dumps(comments)