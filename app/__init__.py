from flask import Flask
from config import Config
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

import os

app = Flask(__name__)

app.config.from_object(Config) #this inherits the Config class, makes the Flask config be overwritten by this

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)

#mail = Mail(app)

csrf = CSRFProtect(app)



from app import routes, models

