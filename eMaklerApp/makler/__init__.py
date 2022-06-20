from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


import finnhub
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emakler.db'
db = SQLAlchemy(app)
finnhub_client = finnhub.Client(api_key="caitgjqad3i2a9kcigrg")

from makler import routes