
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
            pt.tag_id,
            pt.post_id,
            p.id,
            p.user_id
        FROM Tags t
        JOIN PostTags pt
            on pt.tag_id = t.id
        JOIN Posts p
            on p.id = pt.post_id
        WHERE post_id = ?
        """, (post_id, ))

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['label'])

            tags.append(tag.__dict__)

    return json.dumps(tags)


def get_tags_by_user (user_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label,
            pt.tag_id,
            pt.post_id,
            p.id,
            p.user_id
        FROM Tags t
        JOIN PostTags pt
            on pt.tag_id = t.id
        JOIN Posts p
            on p.id = pt.post_id
        WHERE p.user_id = ?
        """, (user_id, ))

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['label'])

            tags.append(tag.__dict__)

    return json.dumps(tags)


def create_tag(new_tag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags
            (label)
        VALUES
            ( ?);
        """, (new_tag['label']))

        id = db_cursor.lastrowid

        new_tag['id'] = id

    return json.dumps(new_tag)
    

def delete_tag(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM tags
        WHERE id = ?
        """, (id, ))


def update_tag(id, new_tag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Tags
            SET
                label = ?
        WHERE id = ?
        """, (new_tag['label'], id, ))

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
            t.id,
            t.label
        FROM Tags t
        """)

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            tag = Tag(row['id'], row['label'])

            tags.append(tag.__dict__)

    return json.dumps(tags)


def get_all_posttags():
    """Gets all posttags. Mainly for testing on this app"""
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pt.id,
            pt.post_id,
            pt.tag_id
        FROM PostTags pt
        """)

        posttags = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            posttag = PostTag(row['id'], row['post_id'], row['tag_id'])

            posttags.append(posttag.__dict__)

    return json.dumps(posttags)

def create_posttag(new_posttag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO PostTags
            (post_id, tag_id)
        VALUES
            ( ?,?);
        """, (new_posttag['post_id'], new_posttag['tag_id']))

        id = db_cursor.lastrowid

        new_posttag['id'] = id

    return json.dumps(new_posttag)

def delete_posttag(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM PostTags
        WHERE id = ?
        """, (id, ))