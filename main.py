from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from decimal import Decimal
from werkzeug.security import check_password_hash, generate_password_hash
from bank_app.bank.models import db, User, Account, get_db
from bank_app.bank.auth import login_required
import sqlite3

currencies = {
  "RUB": "₽",  # Russian ruble
  "USD": "$",  # American dollar
  "EUR": "€",  # European euro
  "PLN": "zł"  # Polish zloty
}

exchange_rates = {
  'RUB': {
    'USD': Decimal('0.014'),
    'EUR': Decimal('0.012'),
    'PLN': Decimal('0.058'),
    'RUB': Decimal('1.0')
  },
  'USD': {
    'RUB': Decimal('70.50'),
    'EUR': Decimal('0.85'),
    'PLN': Decimal('3.93'),
    'USD': Decimal('1.0')
  },
  'EUR': {
    'RUB': Decimal('82.17'),
    'USD': Decimal('1.18'),
    'PLN': Decimal('4.63'),
    'EUR': Decimal('1.0')
  },
  'PLN': {
    'RUB': Decimal('17.18'),
    'USD': Decimal('0.25'),
    'EUR': Decimal('0.22'),
    'PLN': Decimal('1.0')
  }
}

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank.db"

db.init_app(app)
with app.app_context():
  db.create_all()


def get_exchange_rate(base_currency, target_currency):
  return exchange_rates[base_currency][target_currency]


@app.teardown_appcontext
def close_db(error):
  if hasattr(g, '_database'):
    g._database.close()


@app.route('/')
def index():
  user = User.query.filter_by(id=session.get('user_id')).first()
  return render_template("index.html",
                         currencies=currencies,
                         exchange_rates=exchange_rates,
                         user=user)


@app.route('/personal_area')
@login_required
def personal_area():
  user = User.query.filter_by(id=session.get('user_id')).first()
  print(user)
  users = User.query.filter(User.id != user.id).all()

  users_accounts = {user: user.account for user in users}
  return render_template('personal_area.html',
                         user=user,
                         current_user=user,
                         current_account=user.account,
                         users_accounts=users_accounts)


@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
  sender = request.form.get('sender')
  recipient = request.form.get('recipient')
  amount = Decimal(request.form.get('amount'))

  if sender == recipient:
    return render_template(
      'transfer_error.html',
      message="That's impossible to send money to yourself")
  if amount <= Decimal(0):
    return render_template('transfer_error.html',
                           message="Amount should be positive")

  sender_account = Account.query.filter_by(user_id=session['user_id']).first()
  recipient_user = User.query.filter_by(username=recipient).first()

  if not sender_account:
    return render_template('transfer_error.html',
                           message="Invalid sender account")

  if not recipient_user:
    return render_template('transfer_error.html',
                           message="Invalid recipient account")

  recipient_account = recipient_user.account

  if Decimal(sender_account.balance) < amount:
    return render_template(
      'transfer_error.html',
      message="That's not enough money to perform the transaction")

  # get currency of sender and recipient
  sender_currency = sender_account.currency
  recipient_currency = recipient_account.currency

  if sender_currency == recipient_currency:
    # if sender and recipient have the same currency, transfer directly
    sender_account.balance = str(Decimal(sender_account.balance) - amount)
    recipient_account.balance = str(Decimal(sender_account.balance) + amount)
  else:
    # if sender and recipient have different currencies, convert using exchange rate
    rate = get_exchange_rate(sender_currency, recipient_currency)
    converted_amount = amount * Decimal(rate)
    sender_account.balance = str(Decimal(sender_account.balance) - amount)
    recipient_account.balance = str(
      Decimal(sender_account.balance) + converted_amount)

  db.session.commit()

  return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
      flash('Invalid username or password.')
      return redirect(url_for('login'))

    session['user_id'] = user.id
    flash('You were successfully logged in.')
    return redirect(url_for('index'))

  return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    currency = request.form['currency']
    balance = request.form['balance']

    # Check if username already exists in the database
    user = User.query.filter_by(username=username).first()
    if user is not None:
      error = "Username already exists."
      return render_template('register.html', error=error)

    # Check if passwords match
    if password != confirm_password:
      error = "Passwords do not match."
      return render_template('register.html', error=error)

    # Hash password and insert new user into the database
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # Create an account for the new user
    new_account = Account(currency=currency, balance=balance, user=new_user)
    db.session.add(new_account)
    db.session.commit()

    print(new_account)

    flash('You were successfully registered! Please log in.')
    return redirect(url_for('login'))

  return render_template('register.html', currencies=currencies)


@app.route('/logout')
@login_required
def logout():
  session.pop('user_id', None)
  flash('You were logged out.')
  return redirect(url_for('index'))


app.run(host='0.0.0.0', debug=True, port=81)
