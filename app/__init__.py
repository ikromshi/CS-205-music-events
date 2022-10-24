from ensurepip import bootstrap
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
# from app.config import Config
from flask_mail import Mail
from flask_bootstrap import Bootstrap

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)

from app import routes
