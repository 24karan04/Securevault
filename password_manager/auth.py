from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

def register_user(username, password):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    hashed_pw = generate_password_hash(password)

    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_pw))

    conn.commit()
    conn.close()


def login_user(username, password):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()

    conn.close()

    if user and check_password_hash(user[2], password):
        return user
    return None