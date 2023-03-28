import sqlite3
from flask import g

DATABASE_NAME = 'bank.db'


def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(DATABASE_NAME)
  return db


def execute_sql(sql, *params):
  with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    return cursor.lastrowid


def fetch_one(sql, *params):
  with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute(sql, params)
    return cursor.fetchone()


def fetch_all(sql, *params):
  with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute(sql, params)
    return cursor.fetchall()
