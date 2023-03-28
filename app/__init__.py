from flask import Flask, g
from .config import Config
from app.routes.account import account
from app.routes.auth import auth
from app.models.models import db


def create_app():
  app = Flask(__name__)

  @app.teardown_appcontext
  def close_db(error):
    if hasattr(g, '_database'):
      g._database.close()

  # Add any necessary configuration settings here
  app.config['SECRET_KEY'] = Config.SECRET_KEY
  app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI

  db.init_app(app)
  with app.app_context():
    db.create_all()

  # Register any necessary blueprints here
  app.register_blueprint(account)
  app.register_blueprint(auth)

  return app
