import sqlite3
import json
from models import REACTION, PostReaction

def get_all_reactions():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            r.id,
            r.label,
            r.image_url
        FROM Reactions r
        """)

        reactions = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            reaction = REACTION(row['id'], row['label'], row['image_url'])
            reactions.append(reaction.__dict__)

    return json.dumps(reactions)

def create_reaction(new_reaction):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Reactions
            (label, image_url)
        VALUES
            (?, ?)
        """, (new_reaction['label'], new_reaction['image_url'],))

        id = db_cursor.lastrowid

        new_reaction['id'] = id

    return json.dumps(new_reaction)


def get_all_post_reactions():
    """Gets all post reactions. Mainly for testing on this app"""
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pr.id,
            pr.user_id,
            pr.reaction_id,
            pr.post_id
        FROM PostReactions pr
        """)

        postreactions = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            postreaction = PostReaction(row['id'],row['user_id'], row['reaction_id'], row['post_id'])

            postreactions.append(postreaction.__dict__)

    return json.dumps(postreactions)

def add_post_reaction(postreaction):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO PostReactions
            (user_id, reaction_id, post_id)
        VALUES
            (?, ?, ?)
        """, (postreaction['user_id'], postreaction['reaction_id'],postreaction['post_id']))

        id = db_cursor.lastrowid

        postreaction['id'] = id

    return json.dumps(postreaction)
