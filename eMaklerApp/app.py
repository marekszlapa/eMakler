from flask import Flask, render_template
import finnhub
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

app = Flask(__name__)
finnhub_client = finnhub.Client(api_key="caitgjqad3i2a9kcigrg")
app.config['SECRET_KEY'] = '5202544640dd925e91d97f2a'
# Stock candles


@app.route('/')
@app.route('/home')
def home_page():
    news = finnhub_client.general_news('general')[0]
    return render_template('home.html', news=news)


@app.route('/stock')
def stock_page():
    # cena_appl = finnhub_client.quote('AAPL')["c"]
    lista_akcji = finnhub_client.stock_symbols('US')[0:10]
    cena_appl = list()

    for nazwa in lista_akcji:
        cena_appl.append(finnhub_client.quote(nazwa['symbol'])["c"])
    lista_calosc = zip(lista_akcji, cena_appl)
    # for item in lista_calosc:
    #     print(item)

    return render_template('stock.html', lista_calosc=lista_calosc)

class RegisterForm(FlaskForm):
    username = StringField(label='User Name:')
    email_address = StringField(label='Email Address:')
    password1 = PasswordField(label='Password:')
    password2 = PasswordField(label='Confirm Password:')
    submit = SubmitField(label='Create Account')

@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)