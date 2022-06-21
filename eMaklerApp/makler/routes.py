from makler import app
from flask import render_template, redirect, url_for
from makler.models import Akcje, User
from makler import finnhub_client
from makler.forms import RegisterForm
from makler import db

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

@app.route('/register')
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f'Wystąpił błąd przy tworzeniu konta: {err_msg}')
    return render_template('register.html', form=form)