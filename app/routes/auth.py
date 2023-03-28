from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import User, Account
from app.models.models import db
from app.common.exchange_rates import currencies
from functools import wraps


def login_required(f):

  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'user_id' not in session:
      return redirect(url_for('login'))
    return f(*args, **kwargs)

  return decorated_function


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
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
      return render_template('auth/register.html', error=error)

    # Check if passwords match
    if password != confirm_password:
      error = "Passwords do not match."
      return render_template('auth/register.html', error=error)

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
    return redirect(url_for('auth.login'))

  return render_template('auth/register.html', currencies=currencies)


@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
      flash('Invalid username or password.')
      return redirect(url_for('auth.login'))

    session['user_id'] = user.id
    flash('You were successfully logged in.')
    return redirect(url_for('account.index'))

  return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
  session.pop('user_id', None)
  flash('You were logged out.')
  return redirect(url_for('auth.login'))
