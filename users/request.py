import sqlite3
import json
from models import User, Login
from datetime import datetime


def get_all_users():
    """Gets all users. Mainly for testing on this app"""
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM users u
        """)

        users = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            user = User(row['id'], row['first_name'], row['last_name'], row['bio'], row['username'], row['profile_image_url'], row['created_on'], row['active'], row['email'], row['password'])

            users.append(user.__dict__)

    return json.dumps(users)

def get_single_user(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM users u
        WHERE u.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        user = User(data['id'], data['first_name'], data['last_name'], data['bio'], data['username'], data['profile_image_url'], data['created_on'], data['active'], data['email'], data['password'])

        return json.dumps(user.__dict__)


def create_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Users
            (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (new_user['first_name'], new_user['last_name'], new_user['email'], new_user['bio'], new_user['username'], new_user['password'], new_user['profile_image_url'], datetime.now(), True))

        id = db_cursor.lastrowid

        new_user['id'] = id
        new_user['active'] = True

    return json.dumps(new_user)


def delete_user(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Users
        WHERE id = ?
        """, (id, ))


def update_user(id, new_user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Users
            SET
                first_name = ?,
                last_name = ?,
                email = ?,
                bio = ?,
                username = ?,
                password = ?,
                profile_image_url = ?,
                created_on = ?,
                active = ?
        WHERE id = ?
        """, (new_user['first_name'], new_user['last_name'], new_user['email'], new_user['bio'], new_user['username'], new_user['password'], new_user['profile_image_url'], new_user['created_on'], new_user['active'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def get_user_login(email, password):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.email,
            u.password
        FROM users u
        WHERE u.email = ?
        AND u.password = ?        
        """, (email, password))

        data = db_cursor.fetchone()
        try:
            user = Login(data['email'], data['id'], True)
        except:
            print("login error")
            user = Login("", "", False)

        return json.dumps(user.__dict__)