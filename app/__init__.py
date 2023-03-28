from flask import Flask
from .config import Config
from app.routes.account import account
from app.routes.auth import auth
from app.models.models import db


def create_app():
  app = Flask(__name__)

  # Add any necessary configuration settings here
  app.config.from_object(Config)

  db.init_app(app)
  with app.app_context():
    db.create_all()

  # Register any necessary blueprints here
  app.register_blueprint(account)
  app.register_blueprint(auth)

  return app
