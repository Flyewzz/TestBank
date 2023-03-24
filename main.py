from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from decimal import Decimal
import requests
import sqlite3
from functools import wraps


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


app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

currencies = {
  "RUB": "₽",  # Russian ruble
  "USD": "$",  # American dollar
  "EUR": "€",  # European euro
  "PLN": "zł"  # Polish zloty
}

accounts = {
  "John": {
    "currency": "USD",
    "balance": Decimal("1000")
  },
  "Jane": {
    "currency": "EUR",
    "balance": Decimal("5000")
  },
  "Tom": {
    "currency": "EUR",
    "balance": Decimal("300")
  },
  "Vizier": {
    "currency": "RUB",
    "balance": Decimal("100000")
  },
  "Zelda": {
    "currency": "PLN",
    "balance": Decimal("1000")
  },
  "Perlive": {
    "currency": "PLN",
    "balance": Decimal("1000")
  }
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


@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()


def get_user():
  user_id = session.get('user_id')
  if user_id:
    with sqlite3.connect('bank.db') as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM users WHERE id=?", (user_id, ))
      user = cursor.fetchone()
      if user:
        return {'id': user[0], 'username': user[1], 'password': user[2]}
  return None


def login_required(f):

  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'user_id' not in session:
      return redirect(url_for('login'))
    return f(*args, **kwargs)

  return decorated_function


@app.route('/protected')
@login_required
def protected():
  return 'This page is only accessible to logged-in users.'


@app.route("/")
def index():
  user = get_user()
  print(user)
  return render_template("index.html",
                         accounts=accounts,
                         currencies=currencies,
                         exchange_rates=exchange_rates,
                         user=user)


@app.route('/personal_area')
@login_required
def personal_area():
  user = get_user()
  return render_template('personal_area.html', user=user)


@app.route('/transfer', methods=['POST'])
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

  with get_db() as conn:
    cursor = conn.cursor()

    # check if sender has enough money in their account
    cursor.execute("SELECT balance FROM accounts WHERE username = ?", (sender,))
    sender_balance = cursor.fetchone()[0]
    if amount > sender_balance:
      return render_template(
        'transfer_error.html',
        message="That's not enough money to perform the transaction")

    # get currency of sender and recipient
    cursor.execute("SELECT currency FROM accounts WHERE username = ?", (sender,))
    sender_currency = cursor.fetchone()[0]
    cursor.execute("SELECT currency FROM accounts WHERE username = ?", (recipient,))
    recipient_currency = cursor.fetchone()[0]

    if sender_currency == recipient_currency:
      # if sender and recipient have the same currency, transfer directly
      cursor.execute("UPDATE accounts SET balance = balance - ? WHERE username = ?", (amount, sender))
      cursor.execute("UPDATE accounts SET balance = balance + ? WHERE username = ?", (amount, recipient))
    else:
      # if sender and recipient have different currencies, convert using exchange rate
      rate = get_exchange_rate(sender_currency, recipient_currency)
      converted_amount = amount * rate
      cursor.execute("UPDATE accounts SET balance = balance - ? WHERE username = ?", (amount, sender))
      cursor.execute("UPDATE accounts SET balance = balance + ? WHERE username = ?", (converted_amount, recipient))

    conn.commit()

  return redirect('/')


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
  if request.method == 'POST':
    name = request.form['name']
    currency = request.form['currency']
    balance = request.form['balance']
    accounts[name] = {"currency": currency, "balance": Decimal(balance)}
    return redirect('/')
  else:
    return render_template('add_client.html', currencies=currencies)


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    print(username)
    print(password)

    db = get_db()
    cursor = db.cursor()

    # get the user from the database
    cursor.execute("SELECT * FROM users WHERE username=?", (username, ))
    user = cursor.fetchone()
    print(user)
    # check if the user exists and the password is correct
    if user is not None and check_password_hash(user[2], password):
      session['user_id'] = user[0]
      flash('You were logged in.')
      return redirect(url_for('index'))

    error = 'Invalid username or password.'
    return render_template('login.html', error=error)

  return render_template('login.html')


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    db = get_db()

    # Check if username already exists in the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username, ))
    user = cursor.fetchone()

    if user:
      error = "Username already exists."
      return render_template('register.html', error=error)

    # Check if passwords match
    if password != confirm_password:
      error = "Passwords do not match."
      return render_template('register.html', error=error)

    # Hash password and insert new user into the database
    hashed_password = generate_password_hash(password, method='sha256')
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   (username, hashed_password))
    db.commit()

    return redirect(url_for('login'))

  return render_template('register.html')


def get_exchange_rate(base_currency, target_currency):
  return exchange_rates[base_currency][target_currency]


@app.route('/logout')
def logout():
  session.pop('user_id', None)
  flash('You were logged out.')
  return redirect(url_for('index'))


app.run(host='0.0.0.0', debug=True, port=81)

# First mistake
# 1. Go to: https://replit.com/@Flyewzz/ZeldaBank
# 2. Press: Transfer
# Result: Critical error, page is dead.

# Second error:
# 1. Go to: https://replit.com/@Flyewzz/ZeldaBank
# 2. In the Sender field, enter 0
# 4. Press: Transfer
# Result: Critical error, page is dead.

# Third error:
# 1. Go to: https://replit.com/@Flyewzz/ZeldaBank
# 2. In the Recipient field, enter 0
# 4. Press: Transfer
# Result: Critical error, page is dead.

# Fourth error:
# 1. Go to: https://replit.com/@Flyewzz/ZeldaBank
# 2. In the Sender field, enter John
# 3. In the Recipient field, enter Jane
# 3. In the Amount field, enter 1010
# 4. Press: Transfer
# Expected result: Transfer is not possible.
# Result: John has -10 on his account

# Fifth error:
# 1. Go to: https://replit.com/@Flyewzz/ZeldaBank
# 2. In the Sender field, enter John
# 3. In the Recipient field, enter Tom
# 3. In the Amount field, enter -100
# 4. Press: Transfer
# Expected result: Transfer is not possible.
# Result: John can steal money from Tom's account.

# First mistake
# 1. Go to: https://replit.com/@Flyewzz/ZeldaBank#static/styles.css
# 2. In the Sender field: enter Vizier
# 3. In the Recipient field: enter Jane
# 4. In the Amount field: enter 89599,80
# 5. Press: Transfer
# Expected result: It should be in Vizier's account 10400.2 zł.
# Result: We see a non-existent amount in Vizier's account 10400.199999999997 zł.

# 1. Go to: https://replit.com/@Flyewzz/ZeldaBank#main.py
# 2. In the Sender field: enter John
# 3. In the Recipient field: enter Tom
# 4. In the Amount field: enter 10
# 5. Press: Transfer
# Expected result: There should be 310 on Tom's account and 10 taken from Jim's account
# Result: Critical error, page is dead. The error repeats with every user

# 1. Go to: https://replit.com/@Flyewzz/ZeldaBank#main.py
# 2. Look at the Add Client.
# 3. In the Name field, enter Nobody
# 4. In the Currency field chose USD ($)
# 5. In the Balance field, enter - 10
# 6. Press: ADD CLIENT
# Expected result: We have a negative account
# Result: The account cannot be negative
