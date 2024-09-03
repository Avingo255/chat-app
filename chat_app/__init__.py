from flask import Flask
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'sign_in'

from chat_app import routes, auth
