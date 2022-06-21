from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import finnhub
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emakler.db'
app.config['SECRET_KEY'] = '9b6cd67db047e659c56ac078'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
login_manager.login_message = "Aby uzyskać dostęp do tej strony musisz się zalogować"
finnhub_client = finnhub.Client(api_key="caitgjqad3i2a9kcigrg")

from makler import routes
