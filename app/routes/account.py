from flask import Blueprint, render_template, redirect, request, session, url_for
from decimal import Decimal
from app.models.models import db, User, Account, Transaction
from .auth import login_required
from app.common.exchange_rates import currencies, exchange_rates, get_exchange_rate

account = Blueprint('account', __name__)


@account.route('/')
def index():
  user = User.query.filter_by(id=session.get('user_id')).first()
  return render_template("account/index.html",
                         currencies=currencies,
                         exchange_rates=exchange_rates,
                         user=user)


@account.route('/personal_area')
@login_required
def personal_area():
  user = User.query.filter_by(id=session.get('user_id')).first()
  print(user)
  users = User.query.filter(User.id != user.id).all()

  users_accounts = {user: user.account for user in users}
  return render_template('account/personal_area.html',
                         user=user,
                         current_user=user,
                         current_account=user.account,
                         users_accounts=users_accounts)


@account.route('/transfer', methods=['POST'])
@login_required
def transfer():
  sender = request.form.get('sender')
  recipient = request.form.get('recipient')
  amount = Decimal(request.form.get('amount'))

  if sender == recipient:
    return render_template(
      'account/transfer_error.html',
      message="That's impossible to send money to yourself")
  if amount <= Decimal(0):
    return render_template('account/transfer_error.html',
                           message="Amount should be positive")

  sender_account = Account.query.filter_by(user_id=session['user_id']).first()
  recipient_user = User.query.filter_by(username=recipient).first()

  if not sender_account:
    return render_template('account/transfer_error.html',
                           message="Invalid sender account")

  if not recipient_user:
    return render_template('account/transfer_error.html',
                           message="Invalid recipient account")

  recipient_account = recipient_user.account

  if Decimal(sender_account.balance) < amount:
    return render_template(
      'account/transfer_error.html',
      message="That's not enough money to perform the transaction")

  # get currency of sender and recipient
  sender_currency = sender_account.currency
  recipient_currency = recipient_account.currency

  if sender_currency == recipient_currency:
    # if sender and recipient have the same currency, transfer directly
    sender_account.balance = str(Decimal(sender_account.balance) - amount)
    recipient_account.balance = str(Decimal(sender_account.balance) + amount)
    rate = Decimal(1.0)
  else:
    # if sender and recipient have different currencies, convert using exchange rate
    rate = get_exchange_rate(sender_currency, recipient_currency)
    # amount = 1 000 ₽
    converted_amount = amount * Decimal(rate)  # = 56.78 zł
    sender_account.balance = str(Decimal(sender_account.balance) - amount)
    recipient_account.balance = str(
      Decimal(recipient_account.balance) + converted_amount)


# Create a new transaction record
  transaction = Transaction(sender_id=sender_account.user_id,
                            recipient_id=recipient_user.id,
                            sender_account=sender_account,
                            recipient_account=recipient_account,
                            amount=str(amount),
                            currency=sender_currency,
                            exchange_rate=float(rate))
  db.session.add(transaction)
  db.session.commit()

  return redirect(url_for('account.personal_area'))
