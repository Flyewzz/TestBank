from functools import wraps
from flask import session, redirect, url_for, abort, Blueprint, render_template, request, flash
from app.models.models import db, User, Account
from .auth import login_required


def admin_login_required(func):

  @wraps(func)
  def decorated_function(*args, **kwargs):
    if 'user_id' not in session:
      return redirect(url_for('login'))

    user = User.query.filter_by(id=session.get('user_id')).first()
    if user.is_admin:
      return func(*args, **kwargs)

    return abort(403)

  return decorated_function


admin = Blueprint('admin', __name__)

@admin.route('/block_account', methods=['POST'])
@login_required
def block_account():
  account_id = request.args.get('account_id')
  print(account_id)
  account = Account.query.filter_by(id=account_id).first()
  print(account)

  account.is_blocked = True
  db.session.commit()

  flash(f"Account with ID {account_id} is blocked.")
  return redirect(url_for('admin.backoffice'))


@admin.route('/unblock_account', methods=['POST'])
@login_required
def unblock_account():
  account_id = request.args.get('account_id')
  account = Account.query.filter_by(id=account_id).first()

  account.is_blocked = False
  db.session.commit()

  flash(f"Account with ID {account_id} is unblocked.")
  return redirect(url_for('admin.backoffice'))


@admin.route('/backoffice')
@login_required
def backoffice():
  accounts = Account.query.all()
  return render_template('admin/backoffice.html', accounts=accounts)
