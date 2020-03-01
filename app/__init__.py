from flask import Flask
from config import Config
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from app.click_commands import test

import os

app = Flask(__name__)

app.config.from_object(Config)

app.cli.add_command(test)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)

#mail = Mail(app)

csrf = CSRFProtect(app)



from app import routes, models

