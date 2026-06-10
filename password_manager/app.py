from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib

from auth import register_user, login_user
from encryption import encrypt, decrypt

app = Flask(__name__)
app.secret_key = "supersecretkey"


# =========================
# DATABASE SETUP
# =========================

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS passwords(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        website TEXT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return redirect("/login")


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        try:
            register_user(username, password)
        except:
            pass

        return redirect("/login")

    return render_template("register.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = login_user(username, password)

        if user:
            session["user_id"] = user[0]
            return redirect("/dashboard")

    return render_template("login.html")


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT COUNT(*) FROM passwords WHERE user_id=?",
            (session["user_id"],)
        )
        total_passwords = cur.fetchone()[0]

    except:
        total_passwords = 0

    conn.close()

    return render_template(
        "dashboard.html",
        total_passwords=total_passwords
    )


# =========================
# VAULT
# =========================

@app.route("/vault")
def vault():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM passwords WHERE user_id=?",
            (session["user_id"],)
        )

        data = cur.fetchall()

    except:
        data = []

    conn.close()

    return render_template(
        "vault.html",
        data=data
    )


# =========================
# ADD PASSWORD
# =========================

@app.route("/add", methods=["POST"])
def add_password():

    if "user_id" not in session:
        return redirect("/login")

    website = request.form["website"]
    username = request.form["username"]

    encrypted_password = encrypt(
        request.form["password"]
    )

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO passwords
        (user_id, website, username, password)
        VALUES (?, ?, ?, ?)
    """,
    (
        session["user_id"],
        website,
        username,
        encrypted_password
    ))

    conn.commit()
    conn.close()

    return redirect("/vault")


# =========================
# DELETE PASSWORD
# =========================

@app.route("/delete/<int:id>")
def delete(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM passwords WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/vault")


# =========================
# GENERATOR
# =========================

@app.route("/generator")
def generator():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("generator.html")


# =========================
# SECURITY
# =========================

@app.route("/security")
def security():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("security.html")


# =========================
# CRYPTO
# =========================

@app.route("/crypto", methods=["GET", "POST"])
def crypto():

    if "user_id" not in session:
        return redirect("/login")

    generated_hash = None

    if request.method == "POST":

        text = request.form["text"]

        generated_hash = hashlib.sha256(
            text.encode()
        ).hexdigest()

    return render_template(
        "crypto.html",
        hash=generated_hash
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)
