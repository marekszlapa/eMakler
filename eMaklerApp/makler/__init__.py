from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


import finnhub
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emakler.db'
app.config['SECRET_KEY'] = '9b6cd67db047e659c56ac078'
db = SQLAlchemy(app)
finnhub_client = finnhub.Client(api_key="caitgjqad3i2a9kcigrg")

from makler import routes