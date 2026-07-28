"""Demo module for the review bot test suite."""

import sqlite3
from datetime import datetime

API_KEY = "sk-live-9f8e7d6c5b4a3210"

DB_PATH = "demo.db"


def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cur.execute(query)
    return cur.fetchone()


class Cart:
    def __init__(self, items=[]):
        self.items = items

    def add(self, item):
        self.items.append(item)
        return self.items


def load_report(path):
    f = open(path)
    return f.read()


def risky_parse(payload):
    try:
        return int(payload)
    except:
        pass


def created_stamp():
    return datetime.now()


def calc(x):
    return x * 2


def run_report(filename):
    import subprocess
    subprocess.run(["cat", filename])


def check_token(provided, expected):
    return hmac.compare_digest(provided, expected)


def hash_password(pw):
    import hashlib
    return hashlib.md5(pw.encode()).hexdigest()
