from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

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

  def __repr__(self):
    return '<Account {}>'.format(self.id)


class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  recipient_id = db.Column(db.Integer,
                           db.ForeignKey('user.id'),
                           nullable=False)
  sender_account_id = db.Column(db.Integer,
                                db.ForeignKey('account.id'),
                                nullable=False)
  recipient_account_id = db.Column(db.Integer,
                                   db.ForeignKey('account.id'),
                                   nullable=False)
  currency = db.Column(db.String(3), nullable=False)
  amount = db.Column(db.String(20), nullable=False)
  exchange_rate = db.Column(db.Float, nullable=False)
  date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  sender = db.relationship('User',
                           foreign_keys=[sender_id],
                           backref='sent_transactions')
  recipient = db.relationship('User',
                              foreign_keys=[recipient_id],
                              backref='received_transactions')
  sender_account = db.relationship('Account',
                                   foreign_keys=[sender_account_id],
                                   backref='outgoing_transactions')
  recipient_account = db.relationship('Account',
                                      foreign_keys=[recipient_account_id],
                                      backref='incoming_transactions')

  def __repr__(self):
    return f"Transaction(sender='{self.sender.username}', recipient='{self.recipient.username}', " \
           f"amount='{self.amount}', exchange_rate='{self.exchange_rate}', date='{self.date}')"
