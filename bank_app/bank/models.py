import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from decimal import Decimal
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

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from decimal import Decimal

db = SQLAlchemy()

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    account = db.relationship('Account', backref='user', uselist=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)
      

class Account(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    currency = db.Column(db.String(3))
    balance = db.Column(db.String(20))
    # balance = db.Column(db.Numeric(precision=10, scale=2))

    def __repr__(self):
        return '<Account {}>'.format(self.id)
