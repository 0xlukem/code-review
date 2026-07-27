"""Demo module for the review bot test suite."""

import os
import sqlite3
from datetime import datetime

API_KEY = os.environ["API_KEY"]

DB_PATH = "demo.db"


def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
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
