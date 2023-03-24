from flask import Flask, render_template, request, redirect
from decimal import Decimal
import requests

app = Flask(__name__)

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


@app.route("/")
def main():
  return render_template("index.html",
                         accounts=accounts,
                         currencies=currencies,
                         exchange_rates=exchange_rates)


@app.route('/transfer', methods=['POST'])
def transfer():
  sender = request.form.get('sender')
  recipient = request.form.get('recipient')
  amount = Decimal(request.form.get('amount'))
  sender_currency = accounts[sender]['currency']
  recipient_currency = accounts[recipient]['currency']

  if sender not in accounts or recipient not in accounts:
    return render_template('transfer_error.html',
                           message="Invalid account name")
  if sender == recipient:
    return render_template(
      'transfer_error.html',
      message="That's impossible to send money to yourself")
  if amount <= Decimal(0):
    return render_template('transfer_error.html',
                           message="Amount should be positive")

  if amount > accounts[sender]['balance']:
    return render_template(
      'transfer_error.html',
      message="That's not enough money to perform the transaction")

  if sender_currency == recipient_currency:
    accounts[sender]['balance'] -= amount
    accounts[recipient]['balance'] += amount
  else:
    rate = get_exchange_rate(sender_currency, recipient_currency)
    converted_amount = amount * rate
    accounts[sender]['balance'] -= amount
    accounts[recipient]['balance'] += converted_amount

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


def get_exchange_rate(base_currency, target_currency):
  return exchange_rates[base_currency][target_currency]


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
