import sqlite3
import json
from models import REACTION

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