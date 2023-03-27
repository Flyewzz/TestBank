from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from decimal import Decimal
from werkzeug.security import check_password_hash, generate_password_hash
from .models import db, User, Account
from .auth import login_required

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

def get_exchange_rate(base_currency, target_currency):
  return Decimal('1.0')


@app.teardown_appcontext
def close_db(error):
  if hasattr(g, '_database'):
    g._database.close()


@app.route('/')
def index():
  user = User.query.filter_by(id=session.get('user_id')).first()
  accounts = Account.query.filter_by(user_id=user.id).all()
  return render_template("index.html",
                         accounts=accounts,
                         currencies=currencies,
                         exchange_rates=exchange_rates,
                         user=user)


@app.route('/personal_area')
@login_required
def personal_area():
  user = User.query.filter_by(id=session.get('user_id')).first()
  return render_template('personal_area.html', user=user)


@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
  sender_id = request.form.get('sender_id')
  recipient_id = request.form.get('recipient_id')
  amount = Decimal(request.form.get('amount'))

  if sender_id == recipient_id:
    flash("You can't transfer money to yourself!")
    return redirect(url_for('index'))

  sender = Account.query.get(sender_id)
  recipient = Account.query.get(recipient_id)

  if amount <= Decimal('0'):
    flash("Amount should be positive.")
    return redirect(url_for('index'))

  if sender.balance < amount:
    flash("You don't have enough money to perform the transaction.")
    return redirect(url_for('index'))

  if sender.currency == recipient.currency:
    # If sender and recipient have the same currency, transfer directly
    sender.balance -= amount
    recipient.balance += amount
  else:
    # If sender and recipient have different currencies, convert using exchange rate
    rate = get_exchange_rate(sender.currency, recipient.currency)
    converted_amount = amount * rate
    sender.balance -= amount
    recipient.balance += converted_amount

  db.session.commit()

  flash("Transaction successful!")
  return redirect(url_for('index'))


@app.route('/add_account', methods=['GET', 'POST'])
@login_required
def add_account():
  if request.method == 'POST':
    user = User.query.filter_by(id=session.get('user_id')).first()
    currency = request.form['currency']
    balance = Decimal(request.form['balance'])

    account = Account(user_id=user.id, currency=currency, balance=balance)
    db.session.add(account)
    db.session.commit()

    flash("Account added successfully!")
    return redirect(url_for('index'))
  else:
    return render_template('add_account.html', currencies=currencies)


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

    if not username:
      flash('Username is required')
