import sqlite3
from flask import g


def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect('bank.db')

    # create a cursor object to execute SQL statements
    cursor = db.cursor()
    # create a users table in the database
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                  id INTEGER PRIMARY KEY,
                                  username TEXT,
                                  password TEXT
                             )''')

    # create an accounts table in the database
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                                      id INTEGER PRIMARY KEY,
                                      user_id INTEGER,
                                      currency TEXT,
                                      balance DECIMAL(10, 2),
                                      FOREIGN KEY(user_id) REFERENCES users(id)
                                 )''')
    # commit the changes to the database
    db.commit()
  return db