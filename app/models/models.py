from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

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
